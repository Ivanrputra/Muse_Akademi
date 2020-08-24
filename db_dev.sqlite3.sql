BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "course" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	varchar(256) NOT NULL,
	"description"	text NOT NULL,
	"course_pic"	varchar(100) NOT NULL,
	"start_at"	date NOT NULL,
	"close_at"	date NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"admin_id"	integer NOT NULL,
	"price"	integer NOT NULL,
	"is_publish"	bool NOT NULL,
	"url_meet"	varchar(200),
	FOREIGN KEY("admin_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "exam_project" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"title"	varchar(256) NOT NULL,
	"exam_answer_id"	integer NOT NULL,
	"url_project"	varchar(200) NOT NULL,
	FOREIGN KEY("exam_answer_id") REFERENCES "exam_answer"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "order" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"invoice_no"	varchar(500),
	"price"	integer NOT NULL,
	"status"	varchar(2) NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"course_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"order_pic"	varchar(100),
	"admin_id"	integer,
	FOREIGN KEY("admin_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("course_id") REFERENCES "course"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "category" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(256) NOT NULL,
	"category_pic"	varchar(100)
);
CREATE TABLE IF NOT EXISTS "mentor_data" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"cv"	varchar(100) NOT NULL,
	"ktp"	varchar(100) NOT NULL,
	"npwp"	varchar(100),
	"certification"	varchar(100) NOT NULL,
	"portofolio"	varchar(100) NOT NULL,
	"admin_id"	integer,
	"mentor_id"	integer NOT NULL UNIQUE,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"status"	varchar(2) NOT NULL,
	"no_ktp"	varchar(20) NOT NULL,
	FOREIGN KEY("admin_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("mentor_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"firstname"	varchar(256) NOT NULL,
	"lastname"	varchar(256) NOT NULL,
	"email"	varchar(50) NOT NULL UNIQUE,
	"username"	varchar(256) NOT NULL UNIQUE,
	"is_active"	bool NOT NULL,
	"is_user"	bool NOT NULL,
	"is_staff"	bool NOT NULL,
	"profile_pic"	varchar(100),
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"is_mentor"	bool NOT NULL,
	"address"	text,
	"phone"	varchar(15) NOT NULL,
	"password"	varchar(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "library" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"course_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"summary"	decimal,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("course_id") REFERENCES "course"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "exam_answer" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"answer"	text NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"user_id"	integer NOT NULL,
	"exam_id"	integer NOT NULL,
	"summary"	decimal,
	FOREIGN KEY("exam_id") REFERENCES "exam"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "exam_report" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"ide"	integer NOT NULL,
	"konsep"	integer NOT NULL,
	"desain"	integer NOT NULL,
	"proses"	integer NOT NULL,
	"produk"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"mentor_id"	integer NOT NULL,
	"exam_answer_id"	integer NOT NULL,
	"summary"	decimal NOT NULL,
	FOREIGN KEY("mentor_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("exam_answer_id") REFERENCES "exam_answer"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "session_data" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	varchar(256) NOT NULL,
	"session_id"	integer NOT NULL,
	"attachment"	varchar(100) NOT NULL,
	FOREIGN KEY("session_id") REFERENCES "session"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_summernote_attachment" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"file"	varchar(100) NOT NULL,
	"uploaded"	datetime NOT NULL,
	"name"	varchar(255)
);
CREATE TABLE IF NOT EXISTS "exam" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"question"	text NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"course_id"	integer NOT NULL,
	"close_at"	datetime NOT NULL,
	FOREIGN KEY("course_id") REFERENCES "course"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "social_auth_partial" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"token"	varchar(32) NOT NULL,
	"next_step"	smallint unsigned NOT NULL CHECK("next_step">=0),
	"backend"	varchar(32) NOT NULL,
	"data"	text NOT NULL,
	"timestamp"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "social_auth_code" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"email"	varchar(254) NOT NULL,
	"code"	varchar(32) NOT NULL,
	"verified"	bool NOT NULL,
	"timestamp"	datetime NOT NULL
);
CREATE TABLE IF NOT EXISTS "social_auth_usersocialauth" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"provider"	varchar(32) NOT NULL,
	"uid"	varchar(255) NOT NULL,
	"user_id"	integer NOT NULL,
	"extra_data"	text NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "social_auth_nonce" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"server_url"	varchar(255) NOT NULL,
	"timestamp"	integer NOT NULL,
	"salt"	varchar(65) NOT NULL
);
CREATE TABLE IF NOT EXISTS "social_auth_association" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"server_url"	varchar(255) NOT NULL,
	"handle"	varchar(255) NOT NULL,
	"secret"	varchar(255) NOT NULL,
	"issued"	integer NOT NULL,
	"lifetime"	integer NOT NULL,
	"assoc_type"	varchar(64) NOT NULL
);
CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"day"	varchar(2) NOT NULL,
	"time"	time NOT NULL,
	"mentor_id"	integer NOT NULL,
	FOREIGN KEY("mentor_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "course_category" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"course_id"	integer NOT NULL,
	"category_id"	integer NOT NULL,
	FOREIGN KEY("course_id") REFERENCES "course"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("category_id") REFERENCES "category"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "session_mentor" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"session_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	FOREIGN KEY("session_id") REFERENCES "session"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "session" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	varchar(256) NOT NULL,
	"description"	text NOT NULL,
	"start_at"	datetime NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"course_id"	integer NOT NULL,
	FOREIGN KEY("course_id") REFERENCES "course"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag">=0),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_user_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_groups" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL
);
INSERT INTO "course" VALUES (3,'Course 3','Course. ...','course_pic/3/74e1e7a4-9edc-47a7-96c6-6aee51b82d37.png','2020-10-29','2020-07-29','2020-07-29 05:38:05.043145','2020-07-29 05:38:05.043145',3,100000,0,NULL);
INSERT INTO "course" VALUES (7,'Kursus 1','asdasdasd','course_pic/6/eeee3c1c-ebb2-4764-8fcf-e5870ef9a284.jpg','2020-10-30','2020-11-08','2020-08-30 06:47:48.384657','2020-08-24 07:37:40.224073',6,0,1,'https://zoom.us/j/91418671050?pwd=QzVWZEN4bFNBWUtlMW90ZTROK3k2UT09');
INSERT INTO "course" VALUES (9,'werwerwerwer','werwerewr','course_pic/6/cafd9902-f35d-4704-9a5c-0dd272e87fdd.jpg','2020-10-22','2020-08-29','2020-08-13 07:18:10.807800','2020-08-21 16:22:12.210090',6,9999,1,NULL);
INSERT INTO "course" VALUES (10,'drwerwer','wer','course_pic/6/7c61f9ed-3210-40ac-939f-b44c3f5eb1ae.jpg','2020-10-15','2020-08-22','2020-08-14 16:16:15.810216','2020-08-23 12:51:40.420734',6,0,0,NULL);
INSERT INTO "course" VALUES (11,'Course 4','qwerqwe','course_pic/6/03d06f23-2c93-4074-b734-63051ca4ea6d.jpg','2020-10-21','2020-08-31','2020-08-15 17:58:56.503572','2020-08-23 11:49:47.499126',6,1000,1,NULL);
INSERT INTO "course" VALUES (12,'asdasd','asdasd','course_pic/6/2f2f3f5e-66ff-4ac4-827b-3bd735ab3c5e.jpg','2020-10-19','2020-12-31','2020-08-19 15:10:56.191308','2020-08-23 12:52:39.049687',6,0,1,NULL);
INSERT INTO "course" VALUES (13,'test kursus path','sdfsdfsdf','course_pic/6/dab8086b-df7a-4677-bf0b-d2b65ba042ee.png','2020-08-01','2020-08-30','2020-08-23 16:28:58.480602','2020-08-24 05:02:39.896219',6,50,0,'https://www.google.com/gmail/');
INSERT INTO "course" VALUES (14,'ext','asdasdasd','course_pic/6/4f9862be-3be1-4804-8f41-991c17e75d82.jpg','2020-08-01','2020-08-23','2020-08-23 16:40:00.442541','2020-08-23 16:40:00.442541',6,1000000,0,NULL);
INSERT INTO "exam_project" VALUES (3,'2020-07-31 16:54:59.111364','2020-07-31 16:54:59.111364','Project 2',1,'');
INSERT INTO "exam_project" VALUES (5,'2020-08-03 18:59:00.178853','2020-08-03 18:59:00.178853','kjhgjk',2,'');
INSERT INTO "exam_project" VALUES (10,'2020-08-09 19:08:19.572293','2020-08-09 19:08:19.572293','Project Tambahan',1,'');
INSERT INTO "exam_project" VALUES (11,'2020-08-10 05:07:09.247682','2020-08-10 05:07:09.247682','Project 3',1,'');
INSERT INTO "exam_project" VALUES (12,'2020-08-11 16:26:50.686721','2020-08-11 16:26:50.686721','sdfdfs',1,'');
INSERT INTO "exam_project" VALUES (13,'2020-08-11 16:27:36.102669','2020-08-11 16:27:36.102669','sdfdfs',1,'');
INSERT INTO "exam_project" VALUES (14,'2020-08-11 16:29:18.592548','2020-08-11 16:29:18.592548','sdfdfs',1,'');
INSERT INTO "exam_project" VALUES (15,'2020-08-11 16:30:51.073184','2020-08-11 16:30:51.073184','asdasdasdasdasd',1,'');
INSERT INTO "exam_project" VALUES (16,'2020-08-11 16:54:56.901948','2020-08-11 16:54:56.901948','123123',1,'');
INSERT INTO "exam_project" VALUES (17,'2020-08-11 16:55:33.071294','2020-08-11 16:55:33.071294','asdasd',1,'');
INSERT INTO "exam_project" VALUES (18,'2020-08-11 16:56:47.299518','2020-08-11 16:56:47.299518','Multimedia',1,'');
INSERT INTO "exam_project" VALUES (19,'2020-08-11 16:57:12.804390','2020-08-11 16:57:12.804390','Multimedia',1,'');
INSERT INTO "exam_project" VALUES (20,'2020-08-21 00:13:40.350557','2020-08-21 00:13:40.350557','qweqwe',5,'');
INSERT INTO "exam_project" VALUES (21,'2020-08-21 00:25:38.084334','2020-08-21 00:25:38.084334','kjhkj',5,'http://localhost:8000/examanswer/update/5');
INSERT INTO "exam_project" VALUES (22,'2020-08-23 12:11:04.475758','2020-08-23 12:11:04.475758','asdasd',5,'http://localhost:8000/examanswer/update/5');
INSERT INTO "order" VALUES (16,'INV-6-9-16',9999,'WC','2020-08-23 11:41:56.510093','2020-08-24 07:16:33.125256',9,6,'order_attachment/6/21f0574c-764b-478a-a1f8-b32f7dc8a51b.png',6);
INSERT INTO "category" VALUES (1,'AR / VR','category/img/704df0c7-99ca-43ae-8fac-7cd78c5b6b2a.png');
INSERT INTO "category" VALUES (2,'Multimedia','');
INSERT INTO "category" VALUES (3,'Game','');
INSERT INTO "category" VALUES (4,'Pendidikan','');
INSERT INTO "category" VALUES (5,'Art','');
INSERT INTO "category" VALUES (6,'IoT','');
INSERT INTO "category" VALUES (7,'UI/UX','');
INSERT INTO "category" VALUES (8,'WEB','');
INSERT INTO "mentor_data" VALUES (2,'3/cv/8bf9c445-3c9e-411b-b4ad-e7a9fae0dd69.png','3/ktp/b9bf1aae-2fe6-49b4-ac6f-20d353f72ec7.png','','3/certification/dae77a99-68c6-4d54-8c19-2b245e15cd50.png','3/portofolio/21f96021-98e1-4b8a-ae86-5ad6b80a9afa.png',6,3,'2020-07-23 05:49:34.975424','2020-08-19 17:59:02.202533','DE','');
INSERT INTO "mentor_data" VALUES (3,'9/cv/4c01c64c-9a9c-4e1f-8321-fc3973fbd872.png','9/ktp/af8efc33-68e3-436c-93f1-39cedd8a2814.png','9/npwp/da790ee8-7852-48fd-b3a4-dadcb10affc2.png','9/certification/1a3a024e-deb2-4d84-8043-bd2d64bd9076.png','9/portofolio/ae161976-62b6-4dbb-9d4f-161bfafea976.png',6,1,'2020-07-26 16:59:40.114366','2020-07-30 07:34:29.079906','DE','');
INSERT INTO "mentor_data" VALUES (5,'mentor_data/6/cv/ccae5dae-5b3f-43ca-b059-6f6b61853330.jpg','mentor_data/6/ktp/e94946ca-09f2-46b5-9161-1ce3a733cb22.jpg','mentor_data/6/npwp/b262499c-b600-463f-a423-24593c7cfd4c.jpg','mentor_data/6/certification/507a51b4-4ad6-4965-b672-6129c6a03c70.jpg','mentor_data/6/portofolio/5b046179-3e8a-4c38-897c-334f85b738c9.jpg',6,6,'2020-07-29 04:54:36.954929','2020-08-23 16:58:20.929041','WA','12345678901234567890');
INSERT INTO "mentor_data" VALUES (6,'11/cv/48308bb0-c8a4-43d5-9d66-6711ffc574a9.png','11/ktp/c2eee654-b2fd-48b1-8682-a736d6328a93.png','','11/certification/4b3b0cb6-3a34-4b93-8b67-a89249531fc1.png','11/portofolio/f487e581-e590-415d-a4dc-b7283346b01c.png',6,11,'2020-07-29 05:35:02.403196','2020-08-06 16:24:29.795413','AC','');
INSERT INTO "user" VALUES (1,'2020-07-22 19:44:33.885359',1,'i','p','ivanrputra123@gmail.com','12312313',1,1,1,'','2020-07-22 16:37:29.101876','2020-07-22 16:37:29.117466',0,'','','pbkdf2_sha256$180000$056ji8dTo3WT$pLse0El3pjOX9Zy5jU67Ssrqnq2wqhLK1SN7w+gi5Qs=');
INSERT INTO "user" VALUES (3,NULL,0,'12312312','3123123','aksdjakldj@gmail.com','123',1,1,0,'3/profile_pic/0068b7e6-cc28-40ea-8974-029e7f347120.png','2020-07-22 19:48:29.655897','2020-07-23 05:56:53.779603',0,'','','');
INSERT INTO "user" VALUES (6,'2020-08-23 11:36:35.179503',1,'Ivan','Putra','ivanrputra@gmail.com','ivanrputra',1,1,1,'6/profile_pic/e9b9fb01-f14f-4c22-b1a9-30370ec44b38.jpg','2020-07-23 18:38:19.198718','2020-08-23 16:09:02.206547',1,'Taman Permata Asri K-25 Malang','+6281233655272','pbkdf2_sha256$216000$EuBPhSkhn5Tb$yCm5PbznxyaYaCdz5pswSDkXfVHrGrK2RysIefqFQls=');
INSERT INTO "user" VALUES (7,'2020-08-21 00:42:25.565107',1,'fandi','ar','fandi@gmail.com','fandi',1,1,1,'','2020-07-24 06:17:37.074139','2020-07-24 06:17:37.074139',1,'','','pbkdf2_sha256$216000$EuBPhSkhn5Tb$yCm5PbznxyaYaCdz5pswSDkXfVHrGrK2RysIefqFQls=');
INSERT INTO "user" VALUES (9,'2020-08-21 07:04:03.728802',0,'san','jaya','sanjaya1369@gmail.com','sanjaya1369@gmail.com',1,1,0,'','2020-07-26 16:47:34.472578','2020-07-26 16:50:22.208471',0,'','','pbkdf2_sha256$180000$z32uMri9x2eD$KNyWw0mXAo3Cs3c3uryCvSgKN92ma64AAngk3T6zV4U=');
INSERT INTO "user" VALUES (10,'2020-07-27 05:19:34.411013',0,'koolinera','official','koolinera.official@gmail.com','koolineraofficial10',1,1,0,'','2020-07-27 05:19:34.334509','2020-07-27 05:19:34.343200',0,'','','!PEn3XkADYOeCLUhhhwAw2AkzCk46L8hQcRk8b8IN');
INSERT INTO "user" VALUES (11,'2020-08-21 07:01:59.325207',0,'belajar','id','belajar.bap@gmail.com','belajarid11',1,1,0,'','2020-07-28 06:38:07.202426','2020-07-28 06:38:07.211415',1,'','','!5ggL3H0Ub544BKOOIEB6S7lxxCe7kM3Qa5ZeAs9q');
INSERT INTO "user" VALUES (12,NULL,0,'weqweqw','eqewqwe','eqwqweqwe@gmail.com','qweqweqw',0,1,0,'','2020-08-24 05:17:50.038779','2020-08-24 05:17:50.038779',0,NULL,'','pbkdf2_sha256$216000$iqXtHJD18jOG$NR2U/A+Y/AkzxE9Xobr3Argsg6ECJN6gbo+GtwOzPyg=');
INSERT INTO "library" VALUES (5,'2020-08-06 07:53:59.078860','2020-08-20 18:56:00.827892',7,6,100);
INSERT INTO "library" VALUES (7,'2020-08-19 19:12:28.753420','2020-08-19 19:12:28.753420',11,7,NULL);
INSERT INTO "library" VALUES (9,'2020-08-21 00:42:25.593051','2020-08-21 00:42:25.593051',7,7,NULL);
INSERT INTO "library" VALUES (11,'2020-08-23 11:50:24.477520','2020-08-23 11:50:24.477520',9,6,NULL);
INSERT INTO "exam_answer" VALUES (1,'My Answer is a..','2020-07-31 16:45:59.247199','2020-08-11 18:08:20.671678',6,7,11.3);
INSERT INTO "exam_answer" VALUES (2,'kjgh','2020-08-03 18:59:00.169877','2020-08-10 22:49:02.472415',6,8,50);
INSERT INTO "exam_answer" VALUES (5,'sdfsdfa','2020-08-21 00:13:40.338618','2020-08-23 12:08:58.574047',6,9,NULL);
INSERT INTO "exam_report" VALUES (3,100,100,99,12,44,'2020-08-06 18:46:11.851051','2020-08-06 18:52:58.135270',6,2,71);
INSERT INTO "exam_report" VALUES (10,10,10,10,11,12,'2020-08-10 17:12:39.809247','2020-08-10 17:12:39.809247',7,1,10.6);
INSERT INTO "exam_report" VALUES (13,12,12,12,12,12,'2020-08-11 18:08:20.658712','2020-08-11 18:08:20.658712',6,1,12);
INSERT INTO "session_data" VALUES (3,'Modul',7,'session_attachment/6/b5b554d0-ee57-43f1-8b4d-8cab2cadc7a9.jfif');
INSERT INTO "session_data" VALUES (4,'Modul Tambahan',7,'session_attachment/6/a0e2d5ec-e40f-47bc-bda9-fdad1698171e.jfif');
INSERT INTO "session_data" VALUES (5,'asdasd',5,'session_attachment/6/298e39fa-8f20-4982-a3f1-f56fae33962a.jpg');
INSERT INTO "session_data" VALUES (6,'qaeqwe',5,'session_attachment/6/a1c1eb05-a757-4fba-ad6e-9c062995fa2f.jpg');
INSERT INTO "session_data" VALUES (7,'123',5,'session_attachment/6/5f26773a-7ce0-4673-874b-6f0ef3c1ea9f.jpg');
INSERT INTO "session_data" VALUES (8,'123',18,'session_attachment/13/43d1dcef-48f7-4a35-bccd-9c01d33f903e.jpg');
INSERT INTO "session_data" VALUES (9,'123123',18,'session_attachment/13/58a6518b-1221-4f9f-a757-e1066f991df5.png');
INSERT INTO "django_summernote_attachment" VALUES (1,'django-summernote/2020-07-30/a5ef6bad-28fd-4ba8-ad61-a5ca6e6fd064.png','2020-07-30 05:17:39.808229','Untitled.png');
INSERT INTO "django_summernote_attachment" VALUES (2,'django-summernote/2020-07-30/0809ef77-f71e-4486-aca6-8e95983a1785.png','2020-07-30 05:20:48.171326','Untitled.png');
INSERT INTO "django_summernote_attachment" VALUES (3,'django-summernote/2020-07-31/2696580d-33a7-47e9-b8c2-d40b4ff6457e.jpg','2020-07-30 17:10:23.627646','c3fbc321-a3cc-4219-80e1-fac212f9f4df.jpg');
INSERT INTO "django_summernote_attachment" VALUES (4,'django-summernote/2020-08-15/3586db87-f387-4bb6-94d8-cd165fdb1022.jpg','2020-08-15 16:50:32.946847','613808_3c1c_6.jpg');
INSERT INTO "exam" VALUES (7,'<p>Exam 1 ....</p>','2020-07-30 15:33:42.266728','2020-07-30 15:33:42.266728',7,'2020-07-31 15:33:33');
INSERT INTO "exam" VALUES (8,'<p>Exam 2&nbsp;<img src="/media/django-summernote/2020-07-31/2696580d-33a7-47e9-b8c2-d40b4ff6457e.jpg" style="width: 100px;"></p>','2020-07-30 17:10:33.793464','2020-07-30 17:10:33.793464',7,'2020-07-31 17:10:27');
INSERT INTO "exam" VALUES (9,'<p>asdasd<img src="/media/django-summernote/2020-08-15/3586db87-f387-4bb6-94d8-cd165fdb1022.jpg" style="width: 240px;"></p>','2020-08-15 16:50:38.963981','2020-08-21 00:21:11.575571',7,'2020-11-01 00:17:56');
INSERT INTO "social_auth_usersocialauth" VALUES (1,'google-oauth2','ivanrputra@gmail.com',6,'{"auth_time": 1597940374, "expires": 3599, "token_type": "Bearer", "access_token": "ya29.a0AfH6SMCE0j0kIcjJUpvqO-c-l_DJw5GvigpWz747YYiq_fClHRVrkJC855Zwdce11OCjdI1uRaUI93PZiFD2ubDukTTCyZtpt-WwOmhslJ-rIeRb6vKzi9nSw779ZwsVV8RRMwGvwqU4VBay4o2e2oSHxGSd2Q-x32E"}');
INSERT INTO "social_auth_usersocialauth" VALUES (2,'google-oauth2','koolinera.official@gmail.com',10,'{"auth_time": 1595827174, "expires": 3599, "token_type": "Bearer", "access_token": "ya29.a0AfH6SMDvvsPVy_ixZIugH_MyUn79OxgZXx6YkOGBIjl_CAvny1qBlo37FFlZLx7QveQsW549tS33eOaCQq6k6eI5wbESpNUps1ZYGNnj5cHD6G7pPW5fzLKEKCMDgGt6e7RPc92ccG1Zsytw-S5n0nkAkNCkOhNX7T0"}');
INSERT INTO "social_auth_usersocialauth" VALUES (3,'google-oauth2','belajar.bap@gmail.com',11,'{"auth_time": 1597993319, "expires": 3599, "token_type": "Bearer", "access_token": "ya29.a0AfH6SMBAYDZCndVHw1SjfxXHBN92L4RR8B70LjetKITPPU7vAKkLyzyFr1j-Pu2zVIrb-ny-Vd7OBU5NdATRfh7DEnsYyn2ce0iM-jBP9HQJOOaXAg-Z7AvsHOz38DeVibZmD105G2zAD1rJSpcyhBnFK734oXw3tl0"}');
INSERT INTO "social_auth_usersocialauth" VALUES (4,'google-oauth2','sanjaya1369@gmail.com',9,'{"auth_time": 1597993443, "expires": 3599, "token_type": "Bearer", "access_token": "ya29.a0AfH6SMCZq56WwmKGuVF0sNTibIMhOn9rEaw5zEGlsRA4tPf3KMAzZNtRq8a2sMJFj4s5mrXAHODm8palZ_7zVKfkD5mIt_GcEJ1OMTGbdGiFVyhQefw1bN_pA18rzbwo-_iJX7DttzY1P_-Yis-QvKDb_iDkqqgQmGw"}');
INSERT INTO "schedule" VALUES (1,'SU','00:11:38',3);
INSERT INTO "schedule" VALUES (2,'MO','00:11:38',6);
INSERT INTO "schedule" VALUES (3,'MO','00:11:38',6);
INSERT INTO "schedule" VALUES (4,'MO','00:11:38',6);
INSERT INTO "schedule" VALUES (5,'MO','00:23:38',6);
INSERT INTO "schedule" VALUES (6,'SU','15:28:00',6);
INSERT INTO "course_category" VALUES (3,3,1);
INSERT INTO "course_category" VALUES (7,7,1);
INSERT INTO "course_category" VALUES (9,9,3);
INSERT INTO "course_category" VALUES (10,9,4);
INSERT INTO "course_category" VALUES (11,9,5);
INSERT INTO "course_category" VALUES (12,9,6);
INSERT INTO "course_category" VALUES (13,9,7);
INSERT INTO "course_category" VALUES (14,10,1);
INSERT INTO "course_category" VALUES (15,10,4);
INSERT INTO "course_category" VALUES (16,11,6);
INSERT INTO "course_category" VALUES (17,11,7);
INSERT INTO "course_category" VALUES (18,12,2);
INSERT INTO "course_category" VALUES (19,13,2);
INSERT INTO "course_category" VALUES (20,13,4);
INSERT INTO "course_category" VALUES (21,14,2);
INSERT INTO "session_mentor" VALUES (10,5,6);
INSERT INTO "session_mentor" VALUES (15,7,6);
INSERT INTO "session_mentor" VALUES (16,5,7);
INSERT INTO "session_mentor" VALUES (17,9,6);
INSERT INTO "session_mentor" VALUES (18,13,6);
INSERT INTO "session_mentor" VALUES (19,14,7);
INSERT INTO "session_mentor" VALUES (20,15,11);
INSERT INTO "session_mentor" VALUES (21,15,6);
INSERT INTO "session_mentor" VALUES (22,16,11);
INSERT INTO "session_mentor" VALUES (23,16,6);
INSERT INTO "session_mentor" VALUES (24,17,11);
INSERT INTO "session_mentor" VALUES (25,18,11);
INSERT INTO "session" VALUES (5,'Sesi 1','123123123123','2020-07-29 17:41:00','2020-07-30 06:50:45.186314','2020-08-10 16:55:35.504254',7);
INSERT INTO "session" VALUES (7,'Sesi 2','sesi 2 adalah ...','2020-07-30 17:00:21','2020-07-30 17:00:26.418651','2020-08-10 16:43:55.443526',7);
INSERT INTO "session" VALUES (9,'123123123123','123123123','2020-08-17 18:00:32','2020-08-17 18:00:53.325521','2020-08-17 18:00:53.325521',7);
INSERT INTO "session" VALUES (10,'wrewer','werwer','2020-08-17 18:09:07','2020-08-17 18:09:14.424310','2020-08-17 18:09:14.424310',7);
INSERT INTO "session" VALUES (11,'sdasdasd','asdasd','2020-08-10 18:11:18','2020-08-17 18:11:28.478869','2020-08-17 18:11:28.478869',7);
INSERT INTO "session" VALUES (12,'qweqwe','qweqwe','2020-08-18 04:09:44','2020-08-18 04:09:47.842114','2020-08-18 04:09:47.842114',7);
INSERT INTO "session" VALUES (13,'coba sessi benar','qwe','2020-11-01 04:16:43','2020-08-18 06:29:43.934242','2020-08-18 06:29:43.934242',7);
INSERT INTO "session" VALUES (14,'werwer','werwer','2020-11-01 06:35:05','2020-08-18 06:40:09.887394','2020-08-18 06:40:09.887394',7);
INSERT INTO "session" VALUES (15,'session baru','asdasdasd','2020-11-01 06:25:24','2020-08-19 06:25:58.699713','2020-08-19 06:25:58.699713',7);
INSERT INTO "session" VALUES (16,'session baru','asdasdasd','2020-11-01 06:25:24','2020-08-19 06:27:40.647980','2020-08-19 06:27:40.647980',7);
INSERT INTO "session" VALUES (17,'delete this','qweqweqweqwe','2020-11-01 03:38:08','2020-08-21 03:39:21.039485','2020-08-21 03:39:21.039485',7);
INSERT INTO "session" VALUES (18,'s','sss','2020-08-20 17:00:00','2020-08-23 16:42:05.215479','2020-08-23 16:42:05.215479',13);
INSERT INTO "django_session" VALUES ('unhl3ucn6gda9nthk6mspr7lnwz49pby','MGM1OWI5Njc1MjMyNGE4ZDc3NDEwZDlkOTUzNmZmYjM0MjVjMWM3MTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWRlMzA4YThkYjEyN2E5NzlmMGMxMzAyZWEzZjRjOTE5MjdkNzg4MSJ9','2020-08-05 19:44:33.891343');
INSERT INTO "django_session" VALUES ('r2ty0lyg2p8powj0agh9wr78d3ea006l','NDE3YTdkMTBmN2MxNmJjNTk4NjllMDdjOGE4MDI1MDZhZjZmMTg2Yzp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjlkZGM5MzZlNjVlZGZkYWJiMjUwODc1MGJiM2FkZDE2M2UxZmNjNCJ9','2020-08-06 19:32:12.056778');
INSERT INTO "django_session" VALUES ('9xtq91rfecieprerrcnn7lc5kprkurvi','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-06 19:34:06.699503');
INSERT INTO "django_session" VALUES ('igogfznuu61jj35cwtxfm0r2mi3r1d6b','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-07 05:56:53.837275');
INSERT INTO "django_session" VALUES ('fj80fi84ic06nwnr5l5fheoa0yet9vol','OGJmZGMyOTQwODc3NTVmNDI3Y2EyYTBmOGYwZTEzMzkzY2FhNjI1ZTp7fQ==','2020-08-08 19:18:18.846890');
INSERT INTO "django_session" VALUES ('jwl0rbkgjnqd9b85tr3nkt91ox66fhmj','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 15:26:58.713035');
INSERT INTO "django_session" VALUES ('ooj0w9jm3wp7l9iwxay6jl0ktk997zws','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 15:30:00.684632');
INSERT INTO "django_session" VALUES ('ywv60kjuq8x5016uw88y4wljes4j7zwj','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 15:32:05.831107');
INSERT INTO "django_session" VALUES ('95agiecfz6d2nw8z51ursyw1rz3sqq2l','OGJmZGMyOTQwODc3NTVmNDI3Y2EyYTBmOGYwZTEzMzkzY2FhNjI1ZTp7fQ==','2020-08-09 15:33:49.181057');
INSERT INTO "django_session" VALUES ('mnob88jzo06ww17wduwybyvqaai0qgan','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 15:41:28.638838');
INSERT INTO "django_session" VALUES ('8vxonj6oe9af16yg36624x295viay63i','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 15:42:10.205947');
INSERT INTO "django_session" VALUES ('8n2lsqmuhu82mjgp663ub8r7glop5mxd','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 16:13:56.277024');
INSERT INTO "django_session" VALUES ('pjymk1bb4uwjmjaczhrfinkzs75talhs','OGJmZGMyOTQwODc3NTVmNDI3Y2EyYTBmOGYwZTEzMzkzY2FhNjI1ZTp7fQ==','2020-08-09 16:14:57.926333');
INSERT INTO "django_session" VALUES ('6cw9yg0z5buqoxkmxxlhvt79sb174cy6','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 16:23:29.848333');
INSERT INTO "django_session" VALUES ('xot4zbjohsdva464x3k5gmaaltdpp3vx','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 16:24:00.801866');
INSERT INTO "django_session" VALUES ('4zcgjpep6gjs89q034zqx31r0ogasqb3','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-09 18:39:19.939799');
INSERT INTO "django_session" VALUES ('70960ks6gjau1ywu9e3tpq2wmywjvulc','ZDJhNTNkYjQ2YThkYjRkMDA1YjUxNjEyNmNjNzkyODg5ZTkyYzM5ZTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTFiMzJkOGM1ODUyZjFiOTFiZTAzZWNlYTdiMjE0MmJjNzE0MzdhMCJ9','2020-08-11 19:10:37.381648');
INSERT INTO "django_session" VALUES ('6nq4dlqju6auliz4lsb8s8kb3ijfpdk7','ZjE3ZWYxODI1MzNjNGYzNjNhNWY3OWNiOTJjZGQ4M2Y4ZWVkZmQzMzp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiJUTzFKVEQ1cGFrMzZ1Q293M2ptd29OMGhNRzllWTNKdiIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6ImExYjMyZDhjNTg1MmYxYjkxYmUwM2VjZWE3YjIxNDJiYzcxNDM3YTAiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-12 04:38:08.506166');
INSERT INTO "django_session" VALUES ('h8qxqnfg70y5zb010r3kfa5vkjp3nrpl','ZjA2NWYzZDAwNzMzNDE0NDBjZjRkNTY1ODE1Njg0OWQwYmM1YTNmODp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiJpTk5pcXZpYkt1S2F2Z3NocjQwWmFyemZzWjd6aERTaCIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6ImExYjMyZDhjNTg1MmYxYjkxYmUwM2VjZWE3YjIxNDJiYzcxNDM3YTAiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-17 17:26:02.007256');
INSERT INTO "django_session" VALUES ('0di8t78jm33kmqdhf3r45tvts39wge27','NGFiZGMwNGUwZjljMTg0YmM4NmY1ODMxN2EzNzU0OTZjNjY5Y2UxNTp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiI0YkNQazNGb1kwNHVwY3AzdDVLaEY4dmtPRlJuMzlETyIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6ImExYjMyZDhjNTg1MmYxYjkxYmUwM2VjZWE3YjIxNDJiYzcxNDM3YTAiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-19 15:50:27.458585');
INSERT INTO "django_session" VALUES ('g1kp81edg1vztlrxneaosht7ep7r7jd7','Zjc3ZWRkODgyYmZjYTZhMzE5ZTkzM2ZjY2I2NDEzOTA0YzE1ZGM5Mjp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiJYWUd1ZWpsaUxMd1RSaUZTRDhtZWV1SGk1b3AzTmFiUCIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6ImExYjMyZDhjNTg1MmYxYjkxYmUwM2VjZWE3YjIxNDJiYzcxNDM3YTAiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-20 06:05:36.596276');
INSERT INTO "django_session" VALUES ('t9wbzjje3c9s8dbc0mj0x1y743mjohz0','YTk1NzlhZmQwNThkODNiZjQ0N2RjYzMwYmFiMzc4Mzc3YmViMzBlNDp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiY2UxYjAwZDY5NTE5ZjcwZjlmOTVlNmY5ZTE3ZWUwZjdhN2FkNWYwNyJ9','2020-08-20 18:55:57.579055');
INSERT INTO "django_session" VALUES ('s0ycag3iawlepz8rgdogo8qzf618g6ae','YTk1NzlhZmQwNThkODNiZjQ0N2RjYzMwYmFiMzc4Mzc3YmViMzBlNDp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiY29yZS5jdXN0b21fYXV0aGVudGljYXRpb24uRW1haWxPclVzZXJuYW1lTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiY2UxYjAwZDY5NTE5ZjcwZjlmOTVlNmY5ZTE3ZWUwZjdhN2FkNWYwNyJ9','2020-08-24 05:02:30.247350');
INSERT INTO "django_session" VALUES ('xys03rjh75r9sc1xniz8v637l5l1y6ta','N2QyNGQwNWE2NjQzNWU5OThmNzc3OTU4YzczOTIyMjM1ZTc5MTZjNzp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiI4dEpjYVM2ZmpIRGpsM0ltMXFFdld2aTR5cDdjRU5CdiIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6IjAxNGIxMDBhMGIyYjY0YWFhODY5MThkNjNjYWM3YTBjODQwYTQzNTIiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-24 07:01:18.674553');
INSERT INTO "django_session" VALUES ('x2j2smf7h1vyp858ybqkmvnihd5yg6c5','ZWUzZTBmMTg0NzIxNzMzN2E5MTdlNmRiYmFjYTQyNmJlNWRmYmFhYjp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiJweVp0SmRkZ2pKRmFyTXdRY3lwSW1CYzVkUk52VXJXRyIsIl9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoic29jaWFsX2NvcmUuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaGFzaCI6IjAxNGIxMDBhMGIyYjY0YWFhODY5MThkNjNjYWM3YTBjODQwYTQzNTIiLCJzb2NpYWxfYXV0aF9sYXN0X2xvZ2luX2JhY2tlbmQiOiJnb29nbGUtb2F1dGgyIn0=','2020-08-24 07:02:11.443382');
INSERT INTO "django_session" VALUES ('4pb6zgpfmoqgvrgzac0ur8czcpcbea9x','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k52ti:q8IZzN3I8ZHUlXv_A6sxt7F5xDkB_1MNxqd7nnU0he8','2020-08-24 08:11:10.405423');
INSERT INTO "django_session" VALUES ('2jz5dyy4nrgxnh6iy9ykmrer57arcee7','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k5BAy:9Z1Ss2VbOqkPsBhJnMowre3k3Z7cZyKvBQTWEOMFRKo','2020-08-24 17:01:32.800493');
INSERT INTO "django_session" VALUES ('kwp6rmaxks86lrjux5gjn8bpoikbbcmp','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k5Z7o:HhHhimV0Et4GTOgCh3jEiAEEnsx80-0Zo5n8zTUwkM4','2020-08-25 18:35:52.361284');
INSERT INTO "django_session" VALUES ('mu5sj6szexes9idn2dbow3eozaro7pgr','eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiM05vM3czR3d0aHZyekpLcnJsQThORTFRTXJnYXBQOHYifQ:1k5cTS:ylICagf7KCTNa4bHtvjj0J2GNAj97bla34l6qcRzXMM','2020-08-25 22:10:26.435215');
INSERT INTO "django_session" VALUES ('3khch5m74apnbcwo08e6um67nra0corp','eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiTWx4VHh4TDd0cWswNXF4NmNVaVFBOGtDMkJ3eUlndGcifQ:1k5cVJ:6DeyIEIjmNlJ-1pxWDUKK_-CsTnn9Zx7-8YB2u6Y_vI','2020-08-25 22:12:21.159445');
INSERT INTO "django_session" VALUES ('k91shrbgmtx78w2eclxex4rz80eq0ih6','eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiZGtBTUdaSzVkMXdnaTgxRnZJSlZPa3pIaFprRXNaM0MifQ:1k5cXX:wwognebbmw-onLkPVMlGOiDwVAonqQnyr2w4Iu08r5M','2020-08-25 22:14:39.946121');
INSERT INTO "django_session" VALUES ('1fslefpw9539ahozci70wn7ih4ypu3or','eyJnb29nbGUtb2F1dGgyX3N0YXRlIjoiRDI0STRac2hIS2xqSGVqRnlVY1NxcFMxN0tvN1VMMEYifQ:1k5cip:TM2TpQEr_mT09gEO-_npHoV0KBEq_-rgHOqLhV5rLy0','2020-08-25 22:26:19.369319');
INSERT INTO "django_session" VALUES ('jmat49jqt7ou20byhzdvl2hlj35krx85','.eJxVkEGLwjAQhf9Lzlqybdq03kTRm7qwxWOYTCZNMRowVQqy_32NetieZnjD-95jHqwLofM0D3AbXK7iAAOxBXOrLyO2982BdqNoq_G-Pn-j_zm0-dG6sQ1sxlRyqFukq-rN01JNNQ14oks6xIA9eIXhStlHjdk7Ntu-xn6Zwqd-B9ElqkFZ8KKphUCwWJi81BawRCmk4bxKm7EaqK5RNyQbaxsOlShJS2ktf0I_-S-0hzgoH7r-8q_g5AXs9w9HXV4w:1k5ck7:8FUZusne-PO7GP7FS1GMrtuVHYNl1uhelC4uAY62p6k','2020-08-25 22:27:39.440537');
INSERT INTO "django_session" VALUES ('0wj4un8yc1ed6i3m6xmc0qanuuhk9ryv','.eJxVjcEKwjAQRP8lZynBpE3iUfBYPHkum80uCTYJtOlJ_HeteNDbMI838xATbC1O20rLlII4iUEcfjsPeKeyA6wLdbitreYPp9ISQku1dJcMab4ut7dQINNYA83nr_i3FmGN-0dAo6RyVmsERhWOvWfAHo02QcphT4E9kLXoHRnH7CQMuidvDLMUzxfDJz7M:1k5lAO:kR8Ci_azUNnVicRNwJ5nzUl-lFX1Dm6K47LUUgGP9d4','2020-08-26 07:27:20.712720');
INSERT INTO "django_session" VALUES ('udjhp1kb1j2lzamxglgkpv9r3f9iscv9','.eJxVjcEKwjAQRP8lZynBpE3iUfBYPHkum80uCTYJtOlJ_HeteNDbMI838xATbC1O20rLlII4iUEcfjsPeKeyA6wLdbitreYPp9ISQku1dJcMab4ut7dQINNYA83nr_i3FmGN-0dAo6RyVmsERhWOvWfAHo02QcphT4E9kLXoHRnH7CQMuidvDLMUzxfDJz7M:1k6Ro4:eKZXblvEKXMrnqLpdkq5UGi8PZAKFiKjemGNywmRHec','2020-08-28 04:59:08.036117');
INSERT INTO "django_session" VALUES ('0zkrpy3yy8g6u1ujxcbolj91rixmgr58','.eJxVUNtKxDAQ_Zc8axu3lzS-7YJIEXRxPyBMkklSjMnSpLgg_rvNug_2aYYzcy6cbxLwkskjqTHU5zmayWNN7oiN0Xq8j7BktxMpQ8b1iZ_mF-e--rDvDg92fDfjgTWn8Tgenz7N5fy6EkVhiCXhLCa9UvotJkF9YCiHFNUEXqg4Y3VDU_VnWz1fx9u-mG_5DpIrqlqxhjZ8aFsFRjV610kDqlOsZZrSvmzaSMBhUJIj48ZwCn3boWTMGLqK3vyv0h5SFj7aKfwLuKmgpPAQ7AK2FIGB_PwCZWxp4w:1k6yxt:W7DPsXhAZUPZaSTrQKJlKIkOKFuT4-iDwtiL9LNFbTk','2020-08-29 16:23:29.491497');
INSERT INTO "django_session" VALUES ('2p9imv8foc7j51v890fc3pa4mwi6p8ha','.eJxVkE9PwzAMxb9LztBm_ZeG2wTSbuOAOLBL5LhOW0gT0aRiGuK704wd6MnWs3_vWf5mjs6RPbB8Agc9TeRiTmeYcsHuWO99b-newxKHQoUIkdZV9_ZeNPOXPcFyvIRwfDrt8PFzuux39Poi_WEFVSLUEmhWY7cizVbTgB_k0iB4HMEq9DNlNzVkf7HZ4Vqe9yl8yw8QhuTaoSh5KduqQjBYdkWtDWCNohId503qOqOB2ha1JCGNkRyaqiYthDF8Nb3lX60thKis70f378DNC9jPLySYZ8I:1k7vZ8:s1uTP4q5PX1FNwAv37Iq9_GLyWoqYA8ELJOpO4fcSdY','2020-09-01 06:57:50.324360');
INSERT INTO "django_session" VALUES ('0u7mkonjkgj9qsf1yoyvpy5x8h9nc53w','.eJxVkM1qwzAQhN9F59YW_pPdW0pJStomoeTSk1hJK9tElkIkQ6D03SulOdSnXWb5Zob9JhavgTyRfAILPU5oQ45XmPL5rCBg3pIH0jvXG3x0MIeh4D5EPRI73Xyol8O-2K2_js357RNP20lv68P70Rj2_BpBngg-e7zwUUWkWWoC5AltOngnRzBcugtmd9Vnf7HZ5jb2qxS-5AfwQ3JVkpW07NqqkqBlqYpaaJC1ZBVTlDZpU1oAtq0UHbJO645CU9UoGNOaRtN7_s3agA_cuH60_wouXkB-fgFDDGlJ:1k7vqf:xVMLm3PU0EE_x8Sm1CFwRfPGkvRfRtcfRgb5CvoLcTg','2020-09-01 07:15:57.617302');
INSERT INTO "django_session" VALUES ('lpf2uordpyth9i203btqcswgv17bgd6v','.eJxVkEFPwzAMhf9LztCGpmna3RCaEBxA5cYpchKn7dom05JqQ4j_TjN2oCdbz_7es_xNHF4i2ZF8BgcdzuhijheYc0HuSOd9N-G9hyX2hQwRIq6ry6je4JWd2-aBj0vBj_vP-NG-nNnx8PTVMr6CMhFyCXiSg1mRaqsp0CO6NAheDzBJ7U-Y3dSQ_cVmz9fy_pjCt3wPoU-uRgtGWVOXpQarmSm4sqC5FqUwlFapM1YB1rVWDYrG2oZCVXJUQlhLV9Nb_tV6ghDl5LvB_Ttw8wLy8wtgMmbw:1k7wTo:J5kbWHeEijk8kIO_-MM2uEGyCZ_rV1kSn0sJlJTkYsM','2020-09-01 07:56:24.460493');
INSERT INTO "django_session" VALUES ('yht27zarpcsvehxdw0ijx2mpmg6dppn5','.eJxVkE9rwzAMxb-Lz11i8s_JbjuMHcrYaDcouxhZlpMQx4baLYGx776462E5STzp957QN3O0RPbI8hkc9DSTizktMOeC7VjvfW_pwcMlDoUMESKtq6crgCnsuEynw_HZfu3LBj-W1zbsP_k8vU8rKBMhL4HOctQr0mw1BTiRS4PgcQQr0Z8pu6sh-4vNXm7l7SmFb_kBwpBcNYqSl11bVQgGS13UygDWKCqhOW9Sp40CaltUHYnOmI5DU9WkhDCGr6b3_Ju1hRCl9f3o_h24eQH7-QX3rWeT:1k7wYT:1Goylfnt8ZWLgZ-czjDqyateCtxTRdopFwatR6dJC7k','2020-09-01 08:01:13.197554');
INSERT INTO "django_session" VALUES ('8smqdybxebfkfthdq8mc3so5uq8h7ezb','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k8R5m:CemWIEM-gTVDJe61_LeQdEUb1kJGxd0R3Snj3fjOpRg','2020-09-02 16:37:38.220149');
INSERT INTO "django_session" VALUES ('284i9q0voc7ryp0n1imy8imekghmdwdg','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k8TVa:GlRrVvaGw9SmhJdupwSnAlgSHNSA0k1eWt2T-hiyyfM','2020-09-02 19:12:26.110030');
INSERT INTO "django_session" VALUES ('lljcx4tjp2ptn8rup1y5i91cam982cpi','.eJxVjLEKwjAQQP8ls0hypl50FBzFyblcrnc02CbQppP471Zx0PU93nuYlpbat8ssU5s6czRoNr8sEt8lvwWXSba8zLWMHy-5JqaaSt6eR0rDdbqtQaZRLqWT4fQN_249zf26Cns4CAOKtcxeYwCnzilRE3fBA2FEUbfaxoegqg7QWk8eIjSIyub5AqWyPYg:1k8v8T:J96SIZCAP5vpscBAhXKc95uZ6RjtCibd0okfJOGOTA4','2020-09-04 00:42:25.569081');
INSERT INTO "django_session" VALUES ('iz66nli0pfpqj26mtedxpcsnc2y3w5gw','eyJuZXh0IjoiL21hbmFnZW1lbnQvb3JkZXIvIiwiZ29vZ2xlLW9hdXRoMl9zdGF0ZSI6IjdRQ1Y5Uks3bXpWVGMwUlhqMDcwTG5teldjTkxoSk5OIn0:1k913R:ewMPQdhMi2deErsvoTwrWzIKXtf8BcNimIqVCjwG__w','2020-09-04 07:01:37.830947');
INSERT INTO "django_session" VALUES ('m6lqg6cn6xh9lz07t0ztovu5j6gbjii7','.eJxVjLEKwjAQQP8ls5TkTJroKDiKk3O5XO9osE2gTSfx363ioOt7vPdQHa516NaF5y716qhatftlEenO-S2ozNzQutQyfTznmghrKrk5T5jG63zbgowTX0rP4-kb_t0GXIZtFVo4MIFnrYmsxABGjBFEF_fBAvroWcxmnQ1BRAx4rS1aiOC8F1LPF6UMPYc:1k9oId:s-TZkje6ye4Gc3Iy51TeCz8vbV8eAJca-r77S3--3mA','2020-09-06 11:36:35.225205');
INSERT INTO "django_admin_log" VALUES (1,'2020-07-22 19:45:04.174658','2','123123 123132123','[{"added": {}}]',6,1,1);
INSERT INTO "django_admin_log" VALUES (2,'2020-07-22 19:45:11.514460','2','123123 123132123','',6,1,3);
INSERT INTO "django_admin_log" VALUES (3,'2020-07-22 19:48:29.657890','3','12312312 3123123','[{"added": {}}]',6,1,1);
INSERT INTO "django_admin_log" VALUES (4,'2020-07-22 19:48:55.765462','3','12312312 3123123','[{"changed": {"fields": ["Username"]}}]',6,1,2);
INSERT INTO "django_admin_log" VALUES (5,'2020-07-23 05:47:14.406556','1','aksdjakldj@gmail.com','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (6,'2020-07-23 05:48:06.552039','1','aksdjakldj@gmail.com','',11,1,3);
INSERT INTO "django_admin_log" VALUES (7,'2020-07-23 05:48:41.504450','2','aksdjakldj@gmail.com','[{"added": {}}]',11,1,1);
INSERT INTO "django_admin_log" VALUES (8,'2020-07-23 05:55:02.344592','2','aksdjakldj@gmail.com','[{"changed": {"fields": ["Cv", "Ktp", "Certification", "Portofolio"]}}]',11,1,2);
INSERT INTO "django_admin_log" VALUES (9,'2020-07-23 05:56:53.781631','3','12312312 3123123','[{"changed": {"fields": ["Profile pic"]}}]',6,1,2);
INSERT INTO "django_admin_log" VALUES (10,'2020-07-24 05:32:12.441603','1','AR / VR','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (11,'2020-07-24 17:11:40.137658','1','123','[{"added": {}}]',15,6,1);
INSERT INTO "django_admin_log" VALUES (12,'2020-07-25 19:20:28.619791','1','123123121','[{"added": {}}]',8,6,1);
INSERT INTO "django_admin_log" VALUES (13,'2020-07-25 19:20:57.424755','1','asdasd','[{"added": {}}]',9,6,1);
INSERT INTO "django_admin_log" VALUES (14,'2020-07-27 06:02:04.222587','1','123123121','[{"changed": {"fields": ["Admin"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (15,'2020-07-27 06:02:31.579389','1','123123121','[]',8,6,2);
INSERT INTO "django_admin_log" VALUES (16,'2020-07-27 06:09:00.392050','1','Library object (1)','[{"added": {}}]',10,6,1);
INSERT INTO "django_admin_log" VALUES (17,'2020-07-27 07:28:08.250069','2','asdasdasd','[{"added": {}}]',9,6,1);
INSERT INTO "django_admin_log" VALUES (18,'2020-07-27 07:38:49.941544','2','course 2','[{"added": {}}]',8,6,1);
INSERT INTO "django_admin_log" VALUES (19,'2020-07-27 07:41:17.600655','2','course 2','[{"changed": {"fields": ["Price"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (20,'2020-07-27 17:08:30.099792','3','Library object (3)','[{"added": {}}]',10,6,1);
INSERT INTO "django_admin_log" VALUES (21,'2020-07-27 17:16:49.557124','1','Order object (1)','[{"added": {}}]',13,6,1);
INSERT INTO "django_admin_log" VALUES (22,'2020-07-27 17:17:01.568719','1','Order object (1)','[{"changed": {"fields": ["User"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (23,'2020-07-28 05:29:36.629282','1','123','[{"changed": {"fields": ["Mentor"]}}]',15,6,2);
INSERT INTO "django_admin_log" VALUES (24,'2020-07-29 04:54:36.955908','5','ivanrputra@gmail.com','[{"added": {}}]',11,6,1);
INSERT INTO "django_admin_log" VALUES (25,'2020-07-29 05:38:05.046157','3','Course 3','[{"added": {}}]',8,6,1);
INSERT INTO "django_admin_log" VALUES (26,'2020-07-30 07:46:21.651738','1','AR / VR','[{"changed": {"fields": ["Image"]}}]',7,6,2);
INSERT INTO "django_admin_log" VALUES (27,'2020-08-02 07:52:01.529736','2','Multimedia','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (28,'2020-08-02 07:52:55.999990','3','Game','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (29,'2020-08-02 07:53:04.736902','4','Pendidikan','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (30,'2020-08-02 07:53:11.709699','5','Art','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (31,'2020-08-02 07:53:21.550158','6','IoT','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (32,'2020-08-02 07:53:32.006790','7','UI/UX','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (33,'2020-08-02 07:53:41.285410','8','WEB','[{"added": {}}]',7,6,1);
INSERT INTO "django_admin_log" VALUES (34,'2020-08-03 19:09:55.950299','1','ExamReport object (1)','[{"added": {}}]',29,6,1);
INSERT INTO "django_admin_log" VALUES (35,'2020-08-10 22:45:38.318030','1','ExamAnswer object (1)','[{"changed": {"fields": ["Summary"]}}]',19,6,2);
INSERT INTO "django_admin_log" VALUES (36,'2020-08-10 22:46:00.734050','1','ExamAnswer object (1)','[]',19,6,2);
INSERT INTO "django_admin_log" VALUES (37,'2020-08-10 22:46:45.178274','2','ExamAnswer object (2)','[{"changed": {"fields": ["Summary"]}}]',19,6,2);
INSERT INTO "django_admin_log" VALUES (38,'2020-08-10 22:49:02.480428','2','ExamAnswer object (2)','[{"changed": {"fields": ["Summary"]}}]',19,6,2);
INSERT INTO "django_admin_log" VALUES (39,'2020-08-16 06:13:15.973460','6','Ivan Putra','[{"changed": {"fields": ["Is mentor"]}}]',6,6,2);
INSERT INTO "django_admin_log" VALUES (40,'2020-08-19 15:03:00.742805','7','Order object (7)','[{"changed": {"fields": ["Order pic", "Status"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (41,'2020-08-19 15:03:18.043960','7','Order object (7)','[{"changed": {"fields": ["Order pic"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (42,'2020-08-19 16:23:31.047147','7','Order object (7)','[{"changed": {"fields": ["Status"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (43,'2020-08-19 16:23:45.057489','7','Order object (7)','[{"changed": {"fields": ["Status"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (44,'2020-08-19 16:36:31.431979','11','Course 4','[{"changed": {"fields": ["Price", "Close at"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (45,'2020-08-19 16:36:58.086907','11','Course 4','[{"changed": {"fields": ["Start at"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (46,'2020-08-19 16:37:16.704985','11','Course 4','[{"changed": {"fields": ["Start at", "Close at"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (47,'2020-08-19 16:44:42.821148','8','Order object (8)','',13,6,3);
INSERT INTO "django_admin_log" VALUES (48,'2020-08-19 16:46:43.540864','9','Order object (9)','',13,6,3);
INSERT INTO "django_admin_log" VALUES (49,'2020-08-19 16:48:54.697839','10','Order object (10)','',13,6,3);
INSERT INTO "django_admin_log" VALUES (50,'2020-08-19 16:50:59.373246','11','Order object (11)','',13,6,3);
INSERT INTO "django_admin_log" VALUES (51,'2020-08-19 16:51:47.702913','12','Order object (12)','',13,6,3);
INSERT INTO "django_admin_log" VALUES (52,'2020-08-20 17:50:46.587615','5','Library object (5)','[{"changed": {"fields": ["Summary"]}}]',10,6,2);
INSERT INTO "django_admin_log" VALUES (53,'2020-08-20 18:56:00.829888','5','Ivan Putra -> Kursus 1 -> 100','[{"changed": {"fields": ["Summary"]}}]',10,6,2);
INSERT INTO "django_admin_log" VALUES (54,'2020-08-21 16:21:04.987417','6','Ivan Putra -> werwerwerwer -> None','',10,6,3);
INSERT INTO "django_admin_log" VALUES (55,'2020-08-21 16:22:12.212116','9','werwerwerwer','[{"changed": {"fields": ["Price"]}}]',8,6,2);
INSERT INTO "django_admin_log" VALUES (56,'2020-08-21 16:43:27.768141','15','Order object (15)','[{"changed": {"fields": ["Status"]}}]',13,6,2);
INSERT INTO "django_admin_log" VALUES (57,'2020-08-21 16:53:37.843694','15','Order object (15)','[{"changed": {"fields": ["Status"]}}]',13,6,2);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (21,6,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (22,6,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (23,6,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (24,6,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (25,7,'add_category','Can add category');
INSERT INTO "auth_permission" VALUES (26,7,'change_category','Can change category');
INSERT INTO "auth_permission" VALUES (27,7,'delete_category','Can delete category');
INSERT INTO "auth_permission" VALUES (28,7,'view_category','Can view category');
INSERT INTO "auth_permission" VALUES (29,8,'add_course','Can add course');
INSERT INTO "auth_permission" VALUES (30,8,'change_course','Can change course');
INSERT INTO "auth_permission" VALUES (31,8,'delete_course','Can delete course');
INSERT INTO "auth_permission" VALUES (32,8,'view_course','Can view course');
INSERT INTO "auth_permission" VALUES (33,9,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (34,9,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (35,9,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (36,9,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (37,10,'add_library','Can add library');
INSERT INTO "auth_permission" VALUES (38,10,'change_library','Can change library');
INSERT INTO "auth_permission" VALUES (39,10,'delete_library','Can delete library');
INSERT INTO "auth_permission" VALUES (40,10,'view_library','Can view library');
INSERT INTO "auth_permission" VALUES (41,11,'add_mentordata','Can add mentor data');
INSERT INTO "auth_permission" VALUES (42,11,'change_mentordata','Can change mentor data');
INSERT INTO "auth_permission" VALUES (43,11,'delete_mentordata','Can delete mentor data');
INSERT INTO "auth_permission" VALUES (44,11,'view_mentordata','Can view mentor data');
INSERT INTO "auth_permission" VALUES (45,12,'add_review','Can add review');
INSERT INTO "auth_permission" VALUES (46,12,'change_review','Can change review');
INSERT INTO "auth_permission" VALUES (47,12,'delete_review','Can delete review');
INSERT INTO "auth_permission" VALUES (48,12,'view_review','Can view review');
INSERT INTO "auth_permission" VALUES (49,13,'add_order','Can add order');
INSERT INTO "auth_permission" VALUES (50,13,'change_order','Can change order');
INSERT INTO "auth_permission" VALUES (51,13,'delete_order','Can delete order');
INSERT INTO "auth_permission" VALUES (52,13,'view_order','Can view order');
INSERT INTO "auth_permission" VALUES (53,14,'add_cart','Can add cart');
INSERT INTO "auth_permission" VALUES (54,14,'change_cart','Can change cart');
INSERT INTO "auth_permission" VALUES (55,14,'delete_cart','Can delete cart');
INSERT INTO "auth_permission" VALUES (56,14,'view_cart','Can view cart');
INSERT INTO "auth_permission" VALUES (57,15,'add_schedule','Can add schedule');
INSERT INTO "auth_permission" VALUES (58,15,'change_schedule','Can change schedule');
INSERT INTO "auth_permission" VALUES (59,15,'delete_schedule','Can delete schedule');
INSERT INTO "auth_permission" VALUES (60,15,'view_schedule','Can view schedule');
INSERT INTO "auth_permission" VALUES (61,16,'add_quizchoice','Can add quiz choice');
INSERT INTO "auth_permission" VALUES (62,16,'change_quizchoice','Can change quiz choice');
INSERT INTO "auth_permission" VALUES (63,16,'delete_quizchoice','Can delete quiz choice');
INSERT INTO "auth_permission" VALUES (64,16,'view_quizchoice','Can view quiz choice');
INSERT INTO "auth_permission" VALUES (65,17,'add_quiz','Can add quiz');
INSERT INTO "auth_permission" VALUES (66,17,'change_quiz','Can change quiz');
INSERT INTO "auth_permission" VALUES (67,17,'delete_quiz','Can delete quiz');
INSERT INTO "auth_permission" VALUES (68,17,'view_quiz','Can view quiz');
INSERT INTO "auth_permission" VALUES (69,18,'add_essay','Can add essay');
INSERT INTO "auth_permission" VALUES (70,18,'change_essay','Can change essay');
INSERT INTO "auth_permission" VALUES (71,18,'delete_essay','Can delete essay');
INSERT INTO "auth_permission" VALUES (72,18,'view_essay','Can view essay');
INSERT INTO "auth_permission" VALUES (73,19,'add_essayanswer','Can add essay answer');
INSERT INTO "auth_permission" VALUES (74,19,'change_essayanswer','Can change essay answer');
INSERT INTO "auth_permission" VALUES (75,19,'delete_essayanswer','Can delete essay answer');
INSERT INTO "auth_permission" VALUES (76,19,'view_essayanswer','Can view essay answer');
INSERT INTO "auth_permission" VALUES (77,20,'add_association','Can add association');
INSERT INTO "auth_permission" VALUES (78,20,'change_association','Can change association');
INSERT INTO "auth_permission" VALUES (79,20,'delete_association','Can delete association');
INSERT INTO "auth_permission" VALUES (80,20,'view_association','Can view association');
INSERT INTO "auth_permission" VALUES (81,21,'add_code','Can add code');
INSERT INTO "auth_permission" VALUES (82,21,'change_code','Can change code');
INSERT INTO "auth_permission" VALUES (83,21,'delete_code','Can delete code');
INSERT INTO "auth_permission" VALUES (84,21,'view_code','Can view code');
INSERT INTO "auth_permission" VALUES (85,22,'add_nonce','Can add nonce');
INSERT INTO "auth_permission" VALUES (86,22,'change_nonce','Can change nonce');
INSERT INTO "auth_permission" VALUES (87,22,'delete_nonce','Can delete nonce');
INSERT INTO "auth_permission" VALUES (88,22,'view_nonce','Can view nonce');
INSERT INTO "auth_permission" VALUES (89,23,'add_usersocialauth','Can add user social auth');
INSERT INTO "auth_permission" VALUES (90,23,'change_usersocialauth','Can change user social auth');
INSERT INTO "auth_permission" VALUES (91,23,'delete_usersocialauth','Can delete user social auth');
INSERT INTO "auth_permission" VALUES (92,23,'view_usersocialauth','Can view user social auth');
INSERT INTO "auth_permission" VALUES (93,24,'add_partial','Can add partial');
INSERT INTO "auth_permission" VALUES (94,24,'change_partial','Can change partial');
INSERT INTO "auth_permission" VALUES (95,24,'delete_partial','Can delete partial');
INSERT INTO "auth_permission" VALUES (96,24,'view_partial','Can view partial');
INSERT INTO "auth_permission" VALUES (97,25,'add_sessiondata','Can add session data');
INSERT INTO "auth_permission" VALUES (98,25,'change_sessiondata','Can change session data');
INSERT INTO "auth_permission" VALUES (99,25,'delete_sessiondata','Can delete session data');
INSERT INTO "auth_permission" VALUES (100,25,'view_sessiondata','Can view session data');
INSERT INTO "auth_permission" VALUES (101,18,'add_exam','Can add exam');
INSERT INTO "auth_permission" VALUES (102,18,'change_exam','Can change exam');
INSERT INTO "auth_permission" VALUES (103,18,'delete_exam','Can delete exam');
INSERT INTO "auth_permission" VALUES (104,18,'view_exam','Can view exam');
INSERT INTO "auth_permission" VALUES (105,19,'add_examanswer','Can add exam answer');
INSERT INTO "auth_permission" VALUES (106,19,'change_examanswer','Can change exam answer');
INSERT INTO "auth_permission" VALUES (107,19,'delete_examanswer','Can delete exam answer');
INSERT INTO "auth_permission" VALUES (108,19,'view_examanswer','Can view exam answer');
INSERT INTO "auth_permission" VALUES (109,26,'add_attachment','Can add attachment');
INSERT INTO "auth_permission" VALUES (110,26,'change_attachment','Can change attachment');
INSERT INTO "auth_permission" VALUES (111,26,'delete_attachment','Can delete attachment');
INSERT INTO "auth_permission" VALUES (112,26,'view_attachment','Can view attachment');
INSERT INTO "auth_permission" VALUES (113,27,'add_examdata','Can add exam data');
INSERT INTO "auth_permission" VALUES (114,27,'change_examdata','Can change exam data');
INSERT INTO "auth_permission" VALUES (115,27,'delete_examdata','Can delete exam data');
INSERT INTO "auth_permission" VALUES (116,27,'view_examdata','Can view exam data');
INSERT INTO "auth_permission" VALUES (117,27,'add_examproject','Can add exam project');
INSERT INTO "auth_permission" VALUES (118,27,'change_examproject','Can change exam project');
INSERT INTO "auth_permission" VALUES (119,27,'delete_examproject','Can delete exam project');
INSERT INTO "auth_permission" VALUES (120,27,'view_examproject','Can view exam project');
INSERT INTO "auth_permission" VALUES (121,28,'add_examsummary','Can add exam summary');
INSERT INTO "auth_permission" VALUES (122,28,'change_examsummary','Can change exam summary');
INSERT INTO "auth_permission" VALUES (123,28,'delete_examsummary','Can delete exam summary');
INSERT INTO "auth_permission" VALUES (124,28,'view_examsummary','Can view exam summary');
INSERT INTO "auth_permission" VALUES (125,29,'add_examreport','Can add exam report');
INSERT INTO "auth_permission" VALUES (126,29,'change_examreport','Can change exam report');
INSERT INTO "auth_permission" VALUES (127,29,'delete_examreport','Can delete exam report');
INSERT INTO "auth_permission" VALUES (128,29,'view_examreport','Can view exam report');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (5,'sessions','session');
INSERT INTO "django_content_type" VALUES (6,'core','user');
INSERT INTO "django_content_type" VALUES (7,'core','category');
INSERT INTO "django_content_type" VALUES (8,'core','course');
INSERT INTO "django_content_type" VALUES (9,'core','session');
INSERT INTO "django_content_type" VALUES (10,'core','library');
INSERT INTO "django_content_type" VALUES (11,'core','mentordata');
INSERT INTO "django_content_type" VALUES (12,'core','review');
INSERT INTO "django_content_type" VALUES (13,'core','order');
INSERT INTO "django_content_type" VALUES (14,'core','cart');
INSERT INTO "django_content_type" VALUES (15,'core','schedule');
INSERT INTO "django_content_type" VALUES (16,'core','quizchoice');
INSERT INTO "django_content_type" VALUES (17,'core','quiz');
INSERT INTO "django_content_type" VALUES (18,'core','exam');
INSERT INTO "django_content_type" VALUES (19,'core','examanswer');
INSERT INTO "django_content_type" VALUES (20,'social_django','association');
INSERT INTO "django_content_type" VALUES (21,'social_django','code');
INSERT INTO "django_content_type" VALUES (22,'social_django','nonce');
INSERT INTO "django_content_type" VALUES (23,'social_django','usersocialauth');
INSERT INTO "django_content_type" VALUES (24,'social_django','partial');
INSERT INTO "django_content_type" VALUES (25,'core','sessiondata');
INSERT INTO "django_content_type" VALUES (26,'django_summernote','attachment');
INSERT INTO "django_content_type" VALUES (27,'core','examproject');
INSERT INTO "django_content_type" VALUES (28,'core','examsummary');
INSERT INTO "django_content_type" VALUES (29,'core','examreport');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2020-07-22 16:11:34.349660');
INSERT INTO "django_migrations" VALUES (2,'contenttypes','0002_remove_content_type_name','2020-07-22 16:11:34.359679');
INSERT INTO "django_migrations" VALUES (3,'auth','0001_initial','2020-07-22 16:11:34.369606');
INSERT INTO "django_migrations" VALUES (4,'auth','0002_alter_permission_name_max_length','2020-07-22 16:11:34.377632');
INSERT INTO "django_migrations" VALUES (5,'auth','0003_alter_user_email_max_length','2020-07-22 16:11:34.388555');
INSERT INTO "django_migrations" VALUES (6,'auth','0004_alter_user_username_opts','2020-07-22 16:11:34.393577');
INSERT INTO "django_migrations" VALUES (7,'auth','0005_alter_user_last_login_null','2020-07-22 16:11:34.404539');
INSERT INTO "django_migrations" VALUES (8,'auth','0006_require_contenttypes_0002','2020-07-22 16:11:34.407506');
INSERT INTO "django_migrations" VALUES (9,'auth','0007_alter_validators_add_error_messages','2020-07-22 16:11:34.415512');
INSERT INTO "django_migrations" VALUES (10,'auth','0008_alter_user_username_max_length','2020-07-22 16:11:34.423509');
INSERT INTO "django_migrations" VALUES (11,'auth','0009_alter_user_last_name_max_length','2020-07-22 16:11:34.430490');
INSERT INTO "django_migrations" VALUES (12,'auth','0010_alter_group_name_max_length','2020-07-22 16:11:34.440443');
INSERT INTO "django_migrations" VALUES (13,'auth','0011_update_proxy_permissions','2020-07-22 16:11:34.454407');
INSERT INTO "django_migrations" VALUES (14,'core','0001_initial','2020-07-22 16:11:34.463356');
INSERT INTO "django_migrations" VALUES (15,'admin','0001_initial','2020-07-22 16:11:34.474351');
INSERT INTO "django_migrations" VALUES (16,'admin','0002_logentry_remove_auto_add','2020-07-22 16:11:34.484326');
INSERT INTO "django_migrations" VALUES (17,'admin','0003_logentry_add_action_flag_choices','2020-07-22 16:11:34.493276');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2020-07-22 16:11:34.498264');
INSERT INTO "django_migrations" VALUES (19,'core','0002_auto_20200722_2312','2020-07-22 16:12:37.012394');
INSERT INTO "django_migrations" VALUES (20,'core','0003_auto_20200722_2315','2020-07-22 16:15:37.899450');
INSERT INTO "django_migrations" VALUES (21,'core','0004_auto_20200723_0011','2020-07-22 17:12:19.937708');
INSERT INTO "django_migrations" VALUES (22,'core','0005_auto_20200723_0012','2020-07-22 17:14:48.515969');
INSERT INTO "django_migrations" VALUES (23,'core','0006_auto_20200723_0015','2020-07-22 17:15:43.921825');
INSERT INTO "django_migrations" VALUES (24,'core','0007_auto_20200723_0025','2020-07-22 17:25:59.422811');
INSERT INTO "django_migrations" VALUES (25,'core','0008_auto_20200723_0236','2020-07-22 19:36:41.314292');
INSERT INTO "django_migrations" VALUES (26,'core','0009_mentordata','2020-07-23 05:44:42.727701');
INSERT INTO "django_migrations" VALUES (27,'core','0010_auto_20200723_1249','2020-07-23 05:49:34.992371');
INSERT INTO "django_migrations" VALUES (28,'core','0011_review','2020-07-23 18:36:55.491026');
INSERT INTO "django_migrations" VALUES (29,'core','0012_order','2020-07-24 05:15:51.943878');
INSERT INTO "django_migrations" VALUES (30,'core','0013_auto_20200724_2330','2020-07-24 16:30:31.725866');
INSERT INTO "django_migrations" VALUES (31,'core','0014_course_rating','2020-07-24 16:42:36.737960');
INSERT INTO "django_migrations" VALUES (32,'core','0015_cart','2020-07-24 16:50:21.846086');
INSERT INTO "django_migrations" VALUES (33,'core','0016_schedule','2020-07-24 17:04:26.671345');
INSERT INTO "django_migrations" VALUES (34,'core','0017_mentordata_status','2020-07-25 17:41:54.671181');
INSERT INTO "django_migrations" VALUES (35,'core','0018_essay_essayanswer_quiz_quizchoice','2020-07-25 18:42:45.580637');
INSERT INTO "django_migrations" VALUES (36,'core','0019_auto_20200727_1136','2020-07-27 04:36:46.656970');
INSERT INTO "django_migrations" VALUES (37,'default','0001_initial','2020-07-27 04:56:48.483253');
INSERT INTO "django_migrations" VALUES (38,'social_auth','0001_initial','2020-07-27 04:56:48.483253');
INSERT INTO "django_migrations" VALUES (39,'default','0002_add_related_name','2020-07-27 04:56:48.515281');
INSERT INTO "django_migrations" VALUES (40,'social_auth','0002_add_related_name','2020-07-27 04:56:48.515281');
INSERT INTO "django_migrations" VALUES (41,'default','0003_alter_email_max_length','2020-07-27 04:56:48.527259');
INSERT INTO "django_migrations" VALUES (42,'social_auth','0003_alter_email_max_length','2020-07-27 04:56:48.527259');
INSERT INTO "django_migrations" VALUES (43,'default','0004_auto_20160423_0400','2020-07-27 04:56:48.551286');
INSERT INTO "django_migrations" VALUES (44,'social_auth','0004_auto_20160423_0400','2020-07-27 04:56:48.555257');
INSERT INTO "django_migrations" VALUES (45,'social_auth','0005_auto_20160727_2333','2020-07-27 04:56:48.567255');
INSERT INTO "django_migrations" VALUES (46,'social_django','0006_partial','2020-07-27 04:56:48.583252');
INSERT INTO "django_migrations" VALUES (47,'social_django','0007_code_timestamp','2020-07-27 04:56:48.599285');
INSERT INTO "django_migrations" VALUES (48,'social_django','0008_partial_timestamp','2020-07-27 04:56:48.611285');
INSERT INTO "django_migrations" VALUES (49,'social_django','0003_alter_email_max_length','2020-07-27 04:56:48.623281');
INSERT INTO "django_migrations" VALUES (50,'social_django','0002_add_related_name','2020-07-27 04:56:48.627271');
INSERT INTO "django_migrations" VALUES (51,'social_django','0001_initial','2020-07-27 04:56:48.631268');
INSERT INTO "django_migrations" VALUES (52,'social_django','0004_auto_20160423_0400','2020-07-27 04:56:48.639253');
INSERT INTO "django_migrations" VALUES (53,'social_django','0005_auto_20160727_2333','2020-07-27 04:56:48.647253');
INSERT INTO "django_migrations" VALUES (54,'core','0020_sessiondata','2020-07-27 06:58:51.652537');
INSERT INTO "django_migrations" VALUES (55,'core','0021_auto_20200728_1248','2020-07-28 18:31:35.518564');
INSERT INTO "django_migrations" VALUES (56,'core','0022_auto_20200729_0130','2020-07-28 18:32:12.283778');
INSERT INTO "django_migrations" VALUES (57,'core','0023_auto_20200729_1216','2020-07-29 05:16:59.412324');
INSERT INTO "django_migrations" VALUES (58,'core','0024_course_is_publish','2020-07-29 07:04:01.808852');
INSERT INTO "django_migrations" VALUES (59,'core','0025_exam_close_at','2020-07-30 05:09:02.245601');
INSERT INTO "django_migrations" VALUES (60,'django_summernote','0001_initial','2020-07-30 05:11:57.758052');
INSERT INTO "django_migrations" VALUES (61,'django_summernote','0002_update-help_text','2020-07-30 05:11:57.765980');
INSERT INTO "django_migrations" VALUES (62,'core','0026_auto_20200730_1446','2020-07-30 07:46:03.130372');
INSERT INTO "django_migrations" VALUES (63,'core','0027_auto_20200731_0042','2020-07-30 17:42:28.965080');
INSERT INTO "django_migrations" VALUES (64,'core','0028_sessiondata_attachment','2020-07-30 17:51:31.842898');
INSERT INTO "django_migrations" VALUES (65,'core','0029_examproject_title','2020-07-30 18:16:08.279519');
INSERT INTO "django_migrations" VALUES (66,'core','0030_examsummary','2020-07-31 18:02:12.263297');
INSERT INTO "django_migrations" VALUES (67,'core','0031_examreport','2020-07-31 18:06:33.023036');
INSERT INTO "django_migrations" VALUES (68,'core','0032_auto_20200804_0140','2020-08-03 18:40:22.299782');
INSERT INTO "django_migrations" VALUES (69,'core','0033_auto_20200805_2324','2020-08-06 17:44:18.335479');
INSERT INTO "django_migrations" VALUES (70,'core','0034_auto_20200807_0044','2020-08-06 17:44:18.384084');
INSERT INTO "django_migrations" VALUES (71,'core','0035_auto_20200807_0147','2020-08-06 18:47:23.054485');
INSERT INTO "django_migrations" VALUES (72,'core','0036_auto_20200807_0148','2020-08-06 18:48:55.307771');
INSERT INTO "django_migrations" VALUES (73,'core','0037_auto_20200810_1335','2020-08-10 06:35:04.020204');
INSERT INTO "django_migrations" VALUES (74,'core','0038_auto_20200810_1336','2020-08-10 06:36:02.182416');
INSERT INTO "django_migrations" VALUES (75,'core','0039_auto_20200810_1340','2020-08-10 06:40:54.793576');
INSERT INTO "django_migrations" VALUES (76,'auth','0012_alter_user_first_name_max_length','2020-08-10 07:20:15.472379');
INSERT INTO "django_migrations" VALUES (77,'core','0040_auto_20200810_1435','2020-08-10 07:35:06.581038');
INSERT INTO "django_migrations" VALUES (78,'core','0041_auto_20200810_1441','2020-08-10 07:41:07.006151');
INSERT INTO "django_migrations" VALUES (79,'core','0042_examanswer_report','2020-08-10 16:48:17.684868');
INSERT INTO "django_migrations" VALUES (80,'core','0043_auto_20200810_2349','2020-08-10 16:49:03.666192');
INSERT INTO "django_migrations" VALUES (81,'core','0044_auto_20200811_0534','2020-08-10 22:36:17.408109');
INSERT INTO "django_migrations" VALUES (82,'core','0045_auto_20200811_0537','2020-08-10 22:38:11.369520');
INSERT INTO "django_migrations" VALUES (83,'core','0046_mentordata_no_ktp','2020-08-13 05:18:37.500807');
INSERT INTO "django_migrations" VALUES (84,'core','0047_auto_20200813_1222','2020-08-13 05:22:42.213662');
INSERT INTO "django_migrations" VALUES (85,'core','0048_auto_20200813_1231','2020-08-13 05:31:06.296672');
INSERT INTO "django_migrations" VALUES (86,'core','0049_auto_20200816_0030','2020-08-15 17:30:37.748756');
INSERT INTO "django_migrations" VALUES (87,'core','0050_remove_course_course_type','2020-08-16 15:10:25.282157');
INSERT INTO "django_migrations" VALUES (88,'core','0051_auto_20200816_2218','2020-08-16 15:18:54.933342');
INSERT INTO "django_migrations" VALUES (89,'core','0052_auto_20200819_0102','2020-08-18 18:02:36.646693');
INSERT INTO "django_migrations" VALUES (90,'core','0053_auto_20200819_0102','2020-08-18 18:02:58.408774');
INSERT INTO "django_migrations" VALUES (91,'core','0054_auto_20200819_1302','2020-08-19 06:02:34.155423');
INSERT INTO "django_migrations" VALUES (92,'core','0055_auto_20200819_2342','2020-08-19 16:42:45.047197');
INSERT INTO "django_migrations" VALUES (93,'core','0056_auto_20200820_2300','2020-08-20 19:09:23.110206');
INSERT INTO "django_migrations" VALUES (94,'core','0057_auto_20200821_0723','2020-08-21 00:23:53.594030');
INSERT INTO "django_migrations" VALUES (95,'core','0058_course_url_project','2020-08-24 04:54:06.187567');
INSERT INTO "django_migrations" VALUES (96,'core','0059_auto_20200824_1156','2020-08-24 04:56:53.367702');
CREATE INDEX IF NOT EXISTS "course_admin_id_46f05a51" ON "course" (
	"admin_id"
);
CREATE INDEX IF NOT EXISTS "exam_project_exam_answer_id_ab59be28" ON "exam_project" (
	"exam_answer_id"
);
CREATE INDEX IF NOT EXISTS "order_admin_id_d9c784a3" ON "order" (
	"admin_id"
);
CREATE INDEX IF NOT EXISTS "order_user_id_e323497c" ON "order" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "order_course_id_4d1bf05c" ON "order" (
	"course_id"
);
CREATE INDEX IF NOT EXISTS "mentor_data_admin_id_fa12f900" ON "mentor_data" (
	"admin_id"
);
CREATE INDEX IF NOT EXISTS "library_user_id_351b72eb" ON "library" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "library_course_id_e6d4c767" ON "library" (
	"course_id"
);
CREATE INDEX IF NOT EXISTS "exam_anwer_exam_id_bf3586f4" ON "exam_answer" (
	"exam_id"
);
CREATE INDEX IF NOT EXISTS "exam_anwer_user_id_616933ff" ON "exam_answer" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "exam_report_exam_answer_id_e1e33525" ON "exam_report" (
	"exam_answer_id"
);
CREATE INDEX IF NOT EXISTS "exam_report_mentor_id_58b3031e" ON "exam_report" (
	"mentor_id"
);
CREATE INDEX IF NOT EXISTS "session_data_session_id_59c344d8" ON "session_data" (
	"session_id"
);
CREATE INDEX IF NOT EXISTS "exam_course_id_60feb579" ON "exam" (
	"course_id"
);
CREATE INDEX IF NOT EXISTS "social_auth_partial_timestamp_50f2119f" ON "social_auth_partial" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "social_auth_partial_token_3017fea3" ON "social_auth_partial" (
	"token"
);
CREATE INDEX IF NOT EXISTS "social_auth_code_timestamp_176b341f" ON "social_auth_code" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "social_auth_code_code_a2393167" ON "social_auth_code" (
	"code"
);
CREATE UNIQUE INDEX IF NOT EXISTS "social_auth_code_email_code_801b2d02_uniq" ON "social_auth_code" (
	"email",
	"code"
);
CREATE UNIQUE INDEX IF NOT EXISTS "social_auth_association_server_url_handle_078befa2_uniq" ON "social_auth_association" (
	"server_url",
	"handle"
);
CREATE INDEX IF NOT EXISTS "social_auth_usersocialauth_user_id_17d28448" ON "social_auth_usersocialauth" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "social_auth_usersocialauth_provider_uid_e6b5e668_uniq" ON "social_auth_usersocialauth" (
	"provider",
	"uid"
);
CREATE UNIQUE INDEX IF NOT EXISTS "social_auth_nonce_server_url_timestamp_salt_f6284463_uniq" ON "social_auth_nonce" (
	"server_url",
	"timestamp",
	"salt"
);
CREATE INDEX IF NOT EXISTS "schedule_mentor_id_2931f69d" ON "schedule" (
	"mentor_id"
);
CREATE INDEX IF NOT EXISTS "course_category_category_id_b58e2462" ON "course_category" (
	"category_id"
);
CREATE INDEX IF NOT EXISTS "course_category_course_id_f1df9811" ON "course_category" (
	"course_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "course_category_course_id_category_id_e695986c_uniq" ON "course_category" (
	"course_id",
	"category_id"
);
CREATE INDEX IF NOT EXISTS "session_mentor_user_id_c6f7ab54" ON "session_mentor" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "session_mentor_session_id_b8f3e528" ON "session_mentor" (
	"session_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "session_mentor_session_id_user_id_2863392b_uniq" ON "session_mentor" (
	"session_id",
	"user_id"
);
CREATE INDEX IF NOT EXISTS "session_course_id_05c7a3a1" ON "session" (
	"course_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "core_user_user_permissions_permission_id_35ccf601" ON "user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "core_user_user_permissions_user_id_085123d3" ON "user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "core_user_user_permissions_user_id_permission_id_73ea0daa_uniq" ON "user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "core_user_groups_group_id_fe8c697f" ON "user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "core_user_groups_user_id_70b4d9b8" ON "user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "core_user_groups_user_id_group_id_c82fcad1_uniq" ON "user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
COMMIT;
