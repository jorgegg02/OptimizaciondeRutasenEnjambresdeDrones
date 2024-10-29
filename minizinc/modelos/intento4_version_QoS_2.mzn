% Parameters

int: numberOfDrones; % Number of drones
int: numberOfRechargePoints; % Number of recharge points
int: numberOfUsersClusters; % Number of users
int: numberOfHAPSs; % Number of HAPSs

int: M1; % Large enough value

int: XY; % maximum xy axis distance
int: CellDist;


set of int: Drones = 1..numberOfDrones; % Set of drones
set of int: RechargePoints = 1..numberOfRechargePoints; % Set of clusters
set of int: Users = 1..numberOfUsersClusters; % Set of users
set of int: HAPSs = 1..numberOfHAPSs; % Set of users

int: RHAPS; % Coverage radius of the HAPSs
array[Drones] of int: Ri; % Coverage radius of drone i
array[Drones] of int: Bi; % Battery capacity of drone i
array[Drones] of int: Ci; % Consumption per unit distance of drone i
array[Users] of int: NUsers; % Number of users in cluster k
array[Users, 1..2] of int: UserClusterPosition; % Position of user cluster k (x, y)



% Decision variables
array[Drones , 1..2] of var 1..XY: DronePosition; % Position of drone i (x, y)
array[Drones] of var 1..3: DroneHeight; % Height of drone 1..3

array[Drones, Users] of var 0..1: UserDroneCoverage; % 1 if drone i covers cluster k, 0 otherwise
array[Users] of var 0..1:isUserCovered; % 1 if covered by any drone, 0 otherwise

array[RechargePoints, 1..2] of var 1..XY: RechargePointPosition; % Position of recharge point k (x, y)
array[Drones] of var RechargePoints: ClosestRP; % [2]= 1 -> closest rechargepoint of drone 2 is rechargepoint 1

array[HAPSs , 1..2] of var 1..XY: HAPSPosition; % Position of HAPS g (x, y)
array[HAPSs, Drones] of var 0..1: DroneHAPSCoverage; % 1 if HAPS g covers drone i, 0 otherwise
% array[Drones] of var HAPSs: ClosestHAPS; % [2] = 1 -> closest HAPS of drone 2 is HAPS 1

array[Users] of var Drones: ClosestDrone; % Height of drone 1..3
array[Users] of var float: userLatency;
array[Users] of var float: userPathLoss;
array[Users] of var float: userBandWidth;


% Helper function to compute euclidean distance
function var int: euclidean(var int: x1,var int: y1, var int: x2, var int: y2) =
    (abs(x1 - x2) + abs(y1 - y2));

% -----------------------Objective function----------------------------------
var int: Objective = pow(sum(k in Users)(isUserCovered[k] * NUsers[k]),2)  
+ round( sum(k in Users)((userBandWidth[k]/25  - userPathLoss[k]   - userLatency[k]) * NUsers[k]) ) 
- sum(i in Drones )(euclidean(DronePosition[i,1], DronePosition[i,2], RechargePointPosition[ClosestRP[i],1], RechargePointPosition[ClosestRP[i], 2]))
                   ;


% Constraints

%-----------------Drone Constraints----------------------------------------------

constraint forall(i in Drones)(
    (Bi[i] / 2) > Ci[i] * (euclidean(DronePosition[i, 1], DronePosition[i, 2], RechargePointPosition[ClosestRP[i], 1], RechargePointPosition[ClosestRP[i], 2]) + DroneHeight[i])
);

constraint forall(i in Drones)(
euclidean(DronePosition[i, 1],DronePosition[i, 2], RechargePointPosition[ClosestRP[i], 1], RechargePointPosition[ClosestRP[i], 2] ) = min(j in RechargePoints)(euclidean(DronePosition[i, 1], DronePosition[i, 2],  RechargePointPosition[j, 1], RechargePointPosition[j, 2] )) 
);

constraint lex_lesseq(DronePosition[Drones,1],[ DronePosition[i,1] | i in reverse(Drones) ]);
constraint lex_lesseq(DronePosition[Drones,2],[ DronePosition[i,2] | i in reverse(Drones) ]);
constraint lex_lesseq(RechargePointPosition[RechargePoints,1],[RechargePointPosition[i,1]|i in reverse(RechargePoints) ]);
constraint lex_lesseq(RechargePointPosition[RechargePoints,2],[RechargePointPosition[i,2]|i in reverse(RechargePoints) ]);

%--------------User Constraints---------------------------------

constraint forall(i in Drones, j in Users)(
    if ( Ri[i] + DroneHeight[i]-1 >= euclidean(DronePosition[i, 1], DronePosition[i, 2], UserClusterPosition[j, 1], UserClusterPosition[j, 2])) then
        
        UserDroneCoverage[i, j] = 1
    else
        UserDroneCoverage[i, j]= 0 % No constraint if sum is 0
    endif
);

constraint forall( k in Users)(
     if (sum(UserDroneCoverage[Drones,k]) > 0) then
        isUserCovered[k] = 1
    else
        isUserCovered[k] = 0 % No constraint if sum is 0
    endif
);



constraint forall(k in Users)(
euclidean(UserClusterPosition[k, 1],UserClusterPosition[k, 2], DronePosition[ClosestDrone[k], 1], DronePosition[ClosestDrone[k], 2] ) = min(i in Drones)(euclidean(UserClusterPosition[k, 1],UserClusterPosition[k, 2],  DronePosition[i, 1], DronePosition[i, 2] )+ DroneHeight[i] ) 
);


%-----------------------HAPS constraints-----------------------------------------------------------
constraint forall(i in Drones, g in HAPSs )(

    RHAPS >= euclidean(DronePosition[i, 1], DronePosition[i, 2], HAPSPosition[g, 1], HAPSPosition[g, 2]) - M1 * (1 - DroneHAPSCoverage[g, i])
);

constraint forall (i in Drones) (
 sum(DroneHAPSCoverage[HAPSs, i]) > 0
);




%----------QoS Constraints-----------------------

constraint forall(k in Users)(
    userLatency[k] =   (euclidean(UserClusterPosition[k, 1],UserClusterPosition[k, 2], DronePosition[ClosestDrone[k], 1], DronePosition[ClosestDrone[k], 2]) + DroneHeight[ClosestDrone[k]])  
);

constraint forall(k in Users)(
    userPathLoss[k] =  userLatency[k]
);

constraint forall(k in Users)(
    userBandWidth[k] =  1000 * isUserCovered[k] / sum (i in Users where ClosestDrone[k] == ClosestDrone[i])(isUserCovered[i]) 
);


% constraint forall(k in Users)(
%     userPathLoss[k] =  37 + 10 * 2.5 * log10(euclidean(UserClusterPosition[k, 1],UserClusterPosition[k, 2], DronePosition[ClosestDrone[k], 1], DronePosition[ClosestDrone[k], 2])^2 + DroneHeight[ClosestDrone[k]]^2)
% );




solve:: int_search(DronePosition, dom_w_deg, indomain_random)
:: int_search(RechargePointPosition, dom_w_deg, indomain_random)
% :: int_search(HAPSPosition, dom_w_deg, indomain_median)
:: restart_luby(250)
:: relax_and_reconstruct(DronePosition[Drones,1]++DronePosition[Drones,2], 75) 
maximize Objective;


% output ["Objective: \(Objective)\n"] ++
% ["RechargePoint \(i): Position: \(RechargePointPosition[i, 1]), \(RechargePointPosition[i, 2])\n" | i in RechargePoints] ++
% ["HAPS \(i): Position: \(HAPSPosition[i, 1]), \(HAPSPosition[i, 2])\n" | i in HAPSs] ++
% ["Drone \(i): Position: \(DronePosition[i, 1]), \(DronePosition[i, 2])\n" | i in Drones] ++
% ["Height of drone \(i): \(DroneHeight[i])\n" | i in Drones] ++
% ["User\(i) Covered: \(isUserCovered[i])\n" | i in Users] ++
 
% [
%   if fix(UserDroneCoverage[i, k]) == 1 then
%     "Drone \(i) covers cluster \(k)?: \(fix(UserDroneCoverage[i, k]))\n"
%   else
%     ""
%   endif
%   | i in Drones, k in Users
% ] ++

% ["Closest recharge point for drone \(i): \(ClosestRP[i])\n" | i in Drones];

%["Drone \(i) covers cluster \(k)?: \(UD[i, k])\n Distance between Drone \(i) and cluster \(k)?: \(euclidean(D[i,1], D[i,2],Pos[k,1],Pos[k,2] ))\n" | i in Drones, k in Users ] ++