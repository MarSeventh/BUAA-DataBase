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
      icon: 'DashboardOutlined',
      renderMenu: true,
      permission: null,
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
      icon: 'ProfileOutlined',
      renderMenu: true,
      cacheable: false,
    },
    component: () => import('@/pages/payList')
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
        component: () => import('@/pages/Signin')
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
