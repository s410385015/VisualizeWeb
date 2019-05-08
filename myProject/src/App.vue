<template>
  <div id="app">
      <SideBar/>
  <!--<router-view/>-->
  </div>
</template>

<script>
import SideBar from './components/SideBar';
export default {
  name: 'App',
  components:{
    SideBar,
  },
}
</script>

<style>
#app {
  min-height: 100vh;
}
.canvas-section {
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
pre {
  color: #2a2a2e;
  background: #fff;
  border-radius: 2px;
  padding: 10px;
  overflow: auto;
}
</style>
