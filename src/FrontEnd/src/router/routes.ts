import { Link } from 'ant-design-vue/lib/anchor';
import { IframeBox } from 'stepin';
import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    redirect: '/home',
    meta: {
      title: '首页',
      renderMenu: false,
      icon: 'CreditCardOutlined',
    },
  },
  {
    path: '/welcome',
    name: '主页',
    meta: {
      renderMenu: true,
      cacheable: false,
      icon: 'HomeOutlined',
    },
    component: () => import('@/pages/welcomePage'),
  },
  {
    path: '/doctorSelect',
    name: '医生选择',
    meta: {
      renderMenu: false,
      cacheable: false,
    },
    component: () => import('@/pages/doctorSelect')
  },
  {
    path: '/departmentSelect',
    name: '挂号预约',
    meta: {
      icon: 'UsergroupAddOutlined',
      renderMenu: true,
      permission: "patient",
      cacheable: true,
    },
    component: () => import('@/pages/departmentSelect')
  },
  {
    path: '/payPage',
    name: '付款界面',
    meta: {
      view: 'blank',
      target: '_blank',
      renderMenu: false,
      cacheable: false,
    },
    component: () => import('@/pages/payPage.vue')
  },
  {
    path: '/payList',
    name: '费用清单',
    meta: {
      icon: 'AccountBookOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "patient",
    },
    component: () => import('@/pages/payList')
  },
  {
    path: '/assayList',
    name: '化验结果查询',
    meta: {
      icon: 'BgColorsOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "patient",
    },
    component: () => import('@/pages/assayList')
  },
  {
    path: '/assayItem',
    name: '化验详情',
    meta: {
      icon: 'ProfileOutlined',
      renderMenu: false,
      cacheable: false,
    },
    component: () => import('@/pages/assayItem')
  },
  {
    path: '/diagnosisList',
    name: '诊断结果查询',
    meta: {
      icon: 'SnippetsOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "patient",
    },
    component: () => import('@/pages/diagnosisList')
  },
  {
    path: '/diagnosisItem',
    name: '诊断详情',
    meta: {
      icon: 'ProfileOutlined',
      renderMenu: false,
      cacheable: false,
    },
    component: () => import('@/pages/diagnosisItem')
  },
  {
    path: '/medicineList',
    name: '开药',
    meta: {
      icon: 'FileAddOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "doctor",
    },
    component: () => import('@/pages/doctor/medicineList/medicineList.vue')
  },
  {
    path: '/analysisList',
    name: '检查项目',
    meta: {
      icon: 'FileDoneOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "doctor",
    },
    component: () => import('@/pages/doctor/analysisList/analysisList.vue')
  },
  {
    path: '/checkResult',
    name: '诊断结果',
    meta: {
      icon: 'ForkOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "doctor",
    },
    component: () => import('@/pages/doctor/checkResult/checkResult.vue')
  },
  {
    path: '/scheduleTable',
    name: '排班日程',
    meta: {
      icon: 'FundProjectionScreenOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "doctor",
    },
    component: () => import('@/pages/doctor/scheduleTable/scheduleTable.vue')
  },
  {
    path: '/addDoctor',
    name: '添加医生',
    meta: {
      icon: 'ContactsOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "admin",
    },
    component: () => import('@/pages/manager/addDoctor/addDoctor.vue')
  },
  {
    path: '/addPatient',
    name: '添加患者',
    meta: {
      icon: 'DeploymentUnitOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "admin",
    },
    component: () => import('@/pages/manager/addPatient/addPatient.vue')
  },
  {
    path: '/searchMedicine',
    name: '管理药品',
    meta: {
      icon: 'ExperimentOutlined',
      renderMenu: true,
      cacheable: false,
      permission: "admin",
    },
    component: () => import('@/pages/manager/searchMedicine/searchMedicine.vue')
  },
  {
    path: '/personal',
    name: '个人中心',
    meta: {
      icon: 'UserOutlined',
      renderMenu: true,
      cacheable: false,
    },
    component: () => import('@/pages/personal')
  },
  {
    path: '/front',
    name: '前端',
    meta: {
      renderMenu: false,
    },
    component: () => import('@/components/layout/FrontView.vue'),
    children: [
      {
        path: '/login',
        name: '登录',
        meta: {
          icon: 'LoginOutlined',
          view: 'blank',
          target: '_blank',
          cacheable: false,
        },
        component: () => import('@/pages/login'),
      },
      {
        path: '/home',
        name: '首页',
        meta: {
          view: 'blank',
        },
        component: () => import('@/pages/home'),
      },
      {
        path: '/signin',
        name: '注册',
        meta: {
          view: 'blank',
          target: '_blank',
          cacheable: false,
        },
        component: () => import('@/pages/signin')
      },
    ],
  },
  {
    path: '/403',
    name: '403',
    props: true,
    meta: {
      renderMenu: false,
    },
    component: () => import('@/pages/Exp403.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    props: true,
    meta: {
      icon: 'CreditCardOutlined',
      renderMenu: false,
      cacheable: false,
      _is404Page: true,
    },
    component: () => import('@/pages/Exp404.vue'),
  },
];

export default routes;
