CREATE TABLE public.employee
(
	id int,
	name varchar,
	date date,
	position varchar,
	   PRIMARY KEY(id)
)

CREATE TABLE public.department
(
	id int ,
	name varchar,
	head_id int ,
	PRIMARY KEY(id),
	CONSTRAINT fk_employee1
      FOREIGN KEY(head_id) 
	  REFERENCES public.employee(id)
	   
	   

)
CREATE TABLE public.dep_empl
(
	dep_id int ,
	empl_id int ,
	CONSTRAINT fk_empl
      FOREIGN KEY(empl_id) 
	  REFERENCES public.employee(id),
	  CONSTRAINT fk_dep
      FOREIGN KEY(dep_id) 
	  REFERENCES public.department(id)
	   

)


