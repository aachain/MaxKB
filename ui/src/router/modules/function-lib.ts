import Layout from '@/layout/layout-template/DetailLayout.vue'
const functionLibRouter = {
  path: '/function-lib',
  name: 'function-lib',
  meta: { title: '工具箱', permission: 'APPLICATION:READ' },
  redirect: '/function-lib',
  component: () => import('@/layout/layout-template/AppLayout.vue'),
  children: [
    {
      path: '/function-lib',
      name: 'function-lib-index',
      meta: { title: '工具箱主页', activeMenu: '/function-lib' },
      component: () => import('@/views/function-lib/index.vue')
    }
  ]
}

export default functionLibRouter
