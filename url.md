# 数据库大作业URL设计

## login

### login/patient

病人登录界面

### login/signup

非社区病人注册界面

### login/doctor

医生登陆界面

### login/admin

管理员登录界面

## menu

菜单

### menu/patientId=xxx

病人端的菜单

#### menu/patientdid=xxx/registration

挂号界面，展示所拥有的科室

##### menu/patientid=xxx/registration/xxx

xxx代表选择的科室，本界面展示该科室的医生以及所在的诊室以及挂号按钮，按下按钮就挂号成功，并且返回menu界面

#### menu/patientid=xxx/query

查询自己的化验结果，显示化验的名称和时间

##### menu/patient=xxx/query/id=xxx

显示id=xxx的具体条数

#### menu/patient=xxx/diagnosis

查询自己的诊断证明，通过时间和医生来判断

##### menu/patient=xxx/diagnosis/diagnosisid=xxx

显示这个诊断的text

#### menu/patientId=xxx/Counter

结算账单

#### menu/patientId=xxx/delete

删除用户，如果是社区用户，显示**你没有这个权限！！！！**

### menu/doctorid=xxx

医生的菜单

#### menu/doctorid=xxxx/MedicinePost

医生开药

#### menu/doctorId=xxxx/LaboratoryPost

医生开化验单

#### menu/doctorId=xxxx/diagnonsisPost

医生下诊断书

#### menu/doctorId=xxxx/dispatch

医生查看自己的排班

### menu/admin

管理员的菜单

#### menu/admin/dispatch

管理员查看各个诊室的排班

#### menu/admin/addDoctor

管理员添加医生id

#### menu/admin/addPatient

管理员添加病人

#### menu/admin/query

管理员查询药品库存量

#### menu/admin/PurchaseMedicine

管理员添加药品