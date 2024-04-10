% Parameters
int: m; % Number of drones
int: p; % Number of recharge points
int: n; % Number of users
int: M1; % Large enough value

int: XY; %maximum xy axis distance


set of int: Drones = 1..m; % Set of drones
set of int: RechargePoints = 1..p; % Set of clusters
set of int: Users = 1..n; % Set of users


array[Drones] of int: Ri; % Coverage radius of drone i
array[Drones] of int: Bi; % Battery capacity of drone i
array[Drones] of int: Ci; % Consumption per unit distance of drone i
array[Users] of int: N; % Number of users in cluster k
array[Users, 1..2] of int: Pos; % Position of user cluster k (x, y)



% Decision variables
array[Drones , 1..2] of var 1..XY: D; % Position of drone i (x, y)
array[Drones, Users] of var 0..1: UD; % 1 if drone i covers cluster k, 0 otherwise
array[Users] of var 0..1:U; % 1 if covered but any drone, 0 otherwise
array[RechargePoints, 1..2] of var 0..XY: P; % Position of recharge point k (x, y)
array[Drones] of var RechargePoints: ClosestRP; % [2]= 1 -> closest rechargepoint of drone 2 is rechargepoint 1
%array[Drones, Users] of var int: Distance; % Distance between drone i and user j


% Helper function to compute euclidean distance
function var int: euclidean(var int: x1,var int: y1, var int: x2, var int: y2) =
    (abs(x1 - x2) + abs(y1 - y2));


% Objective function
var int: Objective = %1000 * sum(k in Users)(U[k] * N[k]) 
                  -  sum(i in Drones )(euclidean(D[i,1], D[i,2], P[ClosestRP[i],1], P[ClosestRP[i], 2]) )
                   ;




% Constraints

constraint forall(i in Drones)(
    ( Bi[i] / 2) > Ci[i] * euclidean(D[i, 1], D[i, 2], P[ClosestRP[i], 1], P[ClosestRP[i], 2]) 
);

constraint forall(i in Drones)(
euclidean(D[i, 1],D[i, 2], P[ClosestRP[i], 1],P[ClosestRP[i], 2] ) = min(j in RechargePoints)(euclidean(D[i, 1], D[i, 2],  P[j, 1], P[j, 2] )) 
  
    % ClosestRP[i] == index_first([jj | jj in RechargePoints where euclidean(D[i, 1], D[i, 2], Pos[jj, 1], Pos[jj, 2]) == min([euclidean(D[i, 1], D[i, 2], Pos[j, 1], Pos[j, 2]) | j in RechargePoints])], 1)
);

constraint forall(i in Drones, j in Users)(
    Ri[i] >= euclidean(D[i, 1], D[i, 2], Pos[j, 1], Pos[j, 2]) - M1 * (1 - UD[i, j])
);

constraint forall( k in Users)(
     if (sum(i in Drones)(UD[i,k]) > 0) then
        U[k] = 1
    else
        U[k] = 0 % No constraint if sum is 0
    endif
);

constraint forall( k in Users)( U[k] == 1);




solve maximize Objective;


output ["Objective: \(Objective)\n"] ++
["Drone \(i): Position: \(D[i, 1]), \(D[i, 2])\n" | i in Drones] ++
["User\(i) Covered: \(U[i])\n" | i in Users] ++
["RechargePoint \(i): Position: \(P[i, 1]), \(P[i, 2])\n" | i in RechargePoints] ++ 
[
  if fix(UD[i, k]) == 1 then
    "Drone \(i) covers cluster \(k)?: \(fix(UD[i, k]))\n"
  else
    ""
  endif
  | i in Drones, k in Users
] ++
["Closest recharge point for drone \(i): \(ClosestRP[i])\n" | i in Drones];

%["Drone \(i) covers cluster \(k)?: \(UD[i, k])\n Distance between Drone \(i) and cluster \(k)?: \(euclidean(D[i,1], D[i,2],Pos[k,1],Pos[k,2] ))\n" | i in Drones, k in Users ] ++