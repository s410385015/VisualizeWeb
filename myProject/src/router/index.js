import Vue from 'vue'
import Router from 'vue-router'
import Graph from '@/components/Graph'
import Data from '@/components/Data'
import TimeSerie from '@/components/TimeSerie'
import HorizonGraphPage from '@/components/HorizonGraphPage'
import DimGraph from '@/components/DimGraph'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/graph',
      name: 'Graph',
      component: Graph
    },
    
    {
      path: '/data',
      name: 'Data',
      component: Data
    },
    
    {
      path: '/timeserie',
      name: 'TimeSerie',
      component: TimeSerie
    },
    {
      path: '/horizongraph',
      name: 'HorizonGraphPage',
      component: HorizonGraphPage
    },
    {
      path: '/dimgraph',
      name: 'DimGraph',
      component: DimGraph
    },
  ]
})
