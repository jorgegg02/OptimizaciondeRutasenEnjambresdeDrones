% Parameters

int: numberOfDrones; % Number of drones
int: numberOfRechargePoints; % Number of recharge points
int: numberOfUsersClusters; % Number of users
int: numberOfHASPs; % Number of HASPs

int: M1; % Large enough value

int: XY; % maximum xy axis distance


set of int: Drones = 1..numberOfDrones; % Set of drones
set of int: RechargePoints = 1..numberOfRechargePoints; % Set of clusters
set of int: Users = 1..numberOfUsersClusters; % Set of users
set of int: HASPs = 1..numberOfHASPs; % Set of users

int: RHASP; % Coverage radius of the HASPs
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

array[HASPs , 1..2] of var 1..XY: HASPPosition; % Position of HASP g (x, y)
array[HASPs, Drones] of var 0..1: DroneHASPCoverage; % 1 if HASP g covers drone i, 0 otherwise
% array[Drones] of var HASPs: ClosestHASP; % [2] = 1 -> closest HASP of drone 2 is HASP 1


% Helper function to compute euclidean distance
function var int: euclidean(var int: x1,var int: y1, var int: x2, var int: y2) =
    (abs(x1 - x2) + abs(y1 - y2));

% Objective function
var int: Objective = 100000 * sum(k in Users)(isUserCovered[k] * NUsers[k]) 
                  -  sum(i in Drones )(euclidean(DronePosition[i,1], DronePosition[i,2], RechargePointPosition[ClosestRP[i],1], RechargePointPosition[ClosestRP[i], 2]) )
                   ;


% Constraints

constraint forall(i in Drones)(
    (Bi[i] / 2) > Ci[i] * (euclidean(DronePosition[i, 1], DronePosition[i, 2], RechargePointPosition[ClosestRP[i], 1], RechargePointPosition[ClosestRP[i], 2]) + DroneHeight[i]*DroneHeight[i]*2)
);

constraint forall(i in Drones)(
euclidean(DronePosition[i, 1],DronePosition[i, 2], RechargePointPosition[ClosestRP[i], 1], RechargePointPosition[ClosestRP[i], 2] ) = min(j in RechargePoints)(euclidean(DronePosition[i, 1], DronePosition[i, 2],  RechargePointPosition[j, 1], RechargePointPosition[j, 2] )) 
);

constraint forall(i in Drones, j in Users)(
    Ri[i]*DroneHeight[i] >= euclidean(DronePosition[i, 1], DronePosition[i, 2], UserClusterPosition[j, 1], UserClusterPosition[j, 2]) - M1 * (1 - UserDroneCoverage[i, j])
);

constraint forall( k in Users)(
     if (sum(i in Drones)(UserDroneCoverage[i,k]) > 0) then
        isUserCovered[k] = 1
    else
        isUserCovered[k] = 0 % No constraint if sum is 0
    endif
);

constraint forall (k in Users) (
 isUserCovered[k] = 1
);

constraint forall(i in Drones)(
euclidean(DronePosition[i, 1],DronePosition[i, 2], RechargePointPosition[ClosestRP[i], 1], RechargePointPosition[ClosestRP[i], 2] ) = min(j in RechargePoints)(euclidean(DronePosition[i, 1], DronePosition[i, 2],  RechargePointPosition[j, 1], RechargePointPosition[j, 2] )) 
);

%-----------------------HASP constraints-----------------------------------------------------------
constraint forall(i in Drones, g in HASPs )(
    RHASP >= euclidean(DronePosition[i, 1], DronePosition[i, 2], HASPPosition[g, 1], HASPPosition[g, 2]) - M1 * (1 - DroneHASPCoverage[g, i])
);

constraint forall (i in Drones) (
 sum(DroneHASPCoverage[HASPs, i]) > 0
);


%todo summetry breaking constraint
%constraint lex_lesseq(DronePosition[d,1],DronePosition[d+1,1]) /\ lex_lesseq(DronePosition[d,2],DronePosition[d+1,2]);



solve:: int_search(DronePosition, dom_w_deg, indomain_random) ::restart_luby(250):: relax_and_reconstruct(DronePosition[Drones,1]++DronePosition[Drones,2], 85) maximize Objective;


% output ["Objective: \(Objective)\n"] ++
% ["RechargePoint \(i): Position: \(RechargePointPosition[i, 1]), \(RechargePointPosition[i, 2])\n" | i in RechargePoints] ++
% ["HASP \(i): Position: \(HASPPosition[i, 1]), \(HASPPosition[i, 2])\n" | i in HASPs] ++
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