import { defineStore } from 'pinia';
import http from './http';
import { Response } from '@/types';
import { useMenuStore } from './menu';
import { useAuthStore } from '@/plugins';

export interface Profile {
  account: Account;
  permission: string[];
  role: string;
}
export interface Account {
  username: string;
  avatar: string;
  gender: number;
  age: number;
  jobtitle?: string;
}

export type TokenResult = {
  token: string;
  expires: number;
};

export type Errorresult = {
}
export const useAccountStore = defineStore('account', {
  state() {
    return {
      account: {} as Account,
      permissions: [] as string[],
      role: '',
      logged: true,
    };
  },
  actions: {
    init() {
      const storedData = localStorage.getItem('user');
      if (storedData) {
        const userData = JSON.parse(storedData);
        const { account, permission, role } = userData;
        this.account = account;
        this.permissions = permission;
        this.role = role;
        this.logged = true; // 用户已经登录
        const { setAuthorities } = useAuthStore();
        setAuthorities(permission);
      }
    },
    async login(username: string, password: string) {
      this.username = username;
      return http
        .request<TokenResult, Response<TokenResult>>('http://127.0.0.1:8000/api/login/', 'post', { username, password })
        .then(async (response) => {
          console.log(response);
          if (response.code === 0) {
            this.logged = true;
            http.setAuthorization(`Bearer ${response.data.token}`, new Date(response.data.expires));
            await this.profile();
            await useMenuStore().getMenuList();
            return response.data;
          } else {
            return Promise.reject(response);
          }
        });
    },
    async signin(username: string, password: string, idcard: string) {
      // 发送注册请求
      return http
        .request<Errorresult, Response<Errorresult>>('http://127.0.0.1:8000/api/signin/', 'post_json', {
          username,
          password,
          idcard,
        })
        .then(async (response) => {
          if (response.code === 200) {
            console.log(response.data);
            return response.data;
          } else {
            return Promise.reject(response);
          }
        });
    },
    async logout() {
      return new Promise<boolean>((resolve) => {
        localStorage.removeItem('stepin-menu');
        localStorage.removeItem('user');
        http.removeAuthorization();
        this.logged = false;
        resolve(true);
      });
    },
    async profile() {
      const username = this.username;
      return http.request<Account, Response<Profile>>(`http://127.0.0.1:8000/api/account?username=${username}`, 'get').then((response) => {
        if (response.code === 200) {
          console.log(response);
          const { setAuthorities } = useAuthStore();
          const { account, permission, role } = response.data;
          this.account = account;
          this.permissions = permission;
          this.role = role;
          setAuthorities(permission);

          // 将用户信息保存在 localStorage 中
          localStorage.setItem('user', JSON.stringify(response.data));
          return response.data;
        } else {
          return Promise.reject(response);
        }
      });
    },
    setLogged(logged: boolean) {
      this.logged = logged;
    },
  },
});
