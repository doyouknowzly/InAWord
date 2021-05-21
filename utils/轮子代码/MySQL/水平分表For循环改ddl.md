```mysql
drop procedure if exists alter_order_ddl;
create procedure alter_order_ddl()
	BEGIN
		declare i int;
		DECLARE table_name VARCHAR(20);
		DECLARE prefix VARCHAR(20);
		set prefix = 'order_';
		set i = 20190220;


		while i > 20131000 DO
			set table_name = CONCAT(prefix, CAST(i AS CHAR));
			select table_name;
			set i = i - 1;

			set @sql = CONCAT('alter table ',table_name," add column `region` varchar(50) DEFAULT '' COMMENT '区域';");
			prepare stmt from @sql;
			execute stmt;

			set @sql2 = CONCAT('alter table ',table_name," add column `brand` varchar(50) DEFAULT '' COMMENT '品牌';");
			prepare stmt2 from @sql2;
			execute stmt2;

			set @sql3 = CONCAT('update ', table_name, " set region = 'ID', brand = 'OPPO' ;" );
			prepare stmt3 from @sql3;
			execute stmt3;

		end while;
	END ;

call alter_order_ddl();
drop procedure  alter_order_ddl;
```

