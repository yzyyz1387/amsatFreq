import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import ChangelogView from '../views/Changelog.vue'
import About from '../views/About.vue'
import DonateUs from '../views/DonateUs.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/changelog',
    name: 'changelog',
    component: ChangelogView
  },
  {
    path: '/about',
    name: 'about',
    component: About
  },
  {
    path: '/donate',
    name: 'donate',
    component: DonateUs
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 