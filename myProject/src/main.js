// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import App from './App'
import router from './router'
import axios from 'axios'
import VueApexCharts from 'vue-apexcharts'
//import BootstrapVue from 'bootstrap-vue'
import HighchartsVue from 'highcharts-vue'

Vue.use(HighchartsVue)
//Vue.use(BootstrapVue)
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

Vue.prototype.$axios = axios

Vue.config.productionTip = false
Vue.use(VueSidebarMenu)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

