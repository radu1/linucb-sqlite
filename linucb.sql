.separator " "
.mode column
.header on

drop table if exists input; -- input (and algorithm constants)
create table input (d int, N int, K int, gamma float, delta float, R float, L float);

drop table if exists x; -- arms
create table x (i int, j int, x_ij float);

drop table if exists theta; -- vector used to draw rewards 
create table theta (j int, theta_j float);

drop table if exists A_inv; -- the first inverse of A
create table A_inv (i int, j int, A_inv_ij float);

-- populate the aforementioned 4 tables
.read "data.sql"


-- https://www.sqlitetutorial.net/sqlite-functions/sqlite-random/
drop view if exists get_noise;
create view get_noise as
  select 1.*random()/9223372036854775807 * (select R from input) as noise;


-- pull = scalar product + noise
drop view if exists pull;
create view pull as
  select i, sum(x_ij * theta_j) + noise as reward
  from theta natural join x, get_noise
  group by i;


-- keep track of pulled arm and reward at each time step
drop table if exists status;
create table status (time_step int, pulled_arm int, reward float);
insert into status values (0, 0, (select(reward) from pull where i=0));


-- vector b
drop table if exists b;
create table b (j int, b_j float);
insert into b 
  select j, x_ij * 
    (select reward from status where time_step = (select max(time_step) from status)) 
  from x where i=0;


-- compute theta_hat based on A_inv and b
drop view if exists theta_hat;
create view theta_hat (j, theta_hat_j) as
  select i, sum(A_inv_ij * b_j)
  from A_inv natural join b
  group by i;


-- compute exploration parameter omega based on algorithm constants
drop view if exists get_omega;
create view get_omega as
  select R * sqrt(d * ln((1+(select max(time_step)+1 from status)*L*L/gamma)/delta)) + sqrt(gamma)*ln((select max(time_step)+1 from status)) as omega
  from input; 


-- compute UCB scores B_i
drop view if exists B_i;
create view B_i (i, score) as
  select i, 
  -- exploitation term
  sum(x0.x_ij * theta_hat_j) + 
  -- exploration term
    (select sqrt(sum(x1.x_ij * v)) * (select omega from get_omega)
      from x x1 natural join
        (select A_inv.j, sum(x2.x_ij * A_inv_ij) as v
        from A_inv join x x2 on (A_inv.i = x2.j)
        where x2.i=x0.i
        group by A_inv.j)
      where x1.i = x0.i)
  from theta_hat natural join x x0
  group by i;


-- return argmax over B_i scores
drop view if exists argmax_B_i;
create view argmax_B_i (i) as
  select i
  from B_i
  where score = (select max(score) from B_i);


-- return the last pulled arm
drop view if exists last_pulled_arm;
create view last_pulled_arm as
  select j, x_ij as val
  from x
  where i = 
    (select pulled_arm 
     from status 
     where time_step = (select max(time_step) from status));


-- a tuple per iteration
drop table if exists iterations;
create table iterations (time_step int);


-- auxiliary tables needed to update A_inv and b
drop table if exists A_inv_aux;
create table A_inv_aux (i int, j int, A_inv_ij float);
drop table if exists A_inv_aux2; 
create table A_inv_aux2 (i int, j int, A_inv_ij float);
drop table if exists b_aux;
create table b_aux (j int, b_j float); 


-- what to do at each exploration-exploitation iteration
create trigger if not exists update_explore_exploit after insert on iterations
begin
  -- pull arm with argmax
  insert into status values (
    1 + (select max(time_step) from status), -- t
    (select i from argmax_B_i), -- pulled arm
    (select(reward) from pull natural join argmax_B_i) -- reward
  );

  -- to substract from A_inv when updating according to Sherman–Morrison formula
  insert into A_inv_aux
  select a as i, c as j, 
  sum (m * n) / 
  (1 + (select sum(aux * val)
    from
      (select i as j, sum (val * A_inv_ij) as aux
      from last_pulled_arm natural join A_inv
      group by i)
      natural join last_pulled_arm))
  from
  (select i as a, j as b, val * aux as m
  from 
    (select i, sum(A_inv_ij * val) as aux
    from A_inv natural join last_pulled_arm 
    group by i)
    ,
    (select j, val
    from last_pulled_arm))
  natural join
  (select i as b, j as c, A_inv_ij as n
  from A_inv)
  group by a, c;
  
  -- update A_inv after keeping in A_inv_aux2 its old version
  insert into A_inv_aux2 select * from A_inv;
  delete from A_inv;
  insert into A_inv
    select i, j, A_inv_aux2.A_inv_ij - A_inv_aux.A_inv_ij
    from A_inv_aux join A_inv_aux2 using (i, j);
  delete from A_inv_aux;
  delete from A_inv_aux2;

  -- update b
  insert into b_aux select * from b;
  delete from b;
  insert into b
    select j, b_j + val * 
      (select reward from status where time_step = (select max(time_step) from status))
    from b_aux natural join last_pulled_arm;
  delete from b_aux;
end; -- end trigger


-- generate n-1 explore-exploit iterations
with recursive
  for(t_step) as (values(0) union all select t_step+1 from for where t_step < (select N from input)-2)
insert into iterations select (t_step) from for; 




--select * from pull;

--select * from status;

--select "Cumulative reward", sum(reward) from status;



-- https://www.sqlite.org/eqp.html
-- .eqp on



