<template>
    <div  id="demo" :class="[{'collapsed' : collapsed}]">
    <div class='demo'>
        <div class="container">
            <h1>
                Demo
                <a
                    style="color: #000;text-transform: uppercase;font-size: 14px;font-weight: 400;"
                    href="https://github.com/s410385015"
                >
                    Github
                </a>
            </h1>
            <hr style="margin: 50px 0px;border: 1px solid #e3e3e3;">
            <keep-alive>
                <router-view />
            </keep-alive>
        </div>
    
        <sidebar-menu :menu="menu"
                :theme="selectedTheme"
                :collapsed="collapsed"
                :show-one-child="true"
                @collapse="onCollapse"
                style="max-width:250px"
        />
    </div>
    </div>
</template>

<script>
import { SidebarMenu } from 'vue-sidebar-menu'
export default {
  name: 'SideBar',
  components: {
    SidebarMenu
  },
  data() {
            return {
                menu: [
                    {
                        header: true,
                        title: 'Main Navigation',
                        
                    },
                    {
                        href: '/data',
                        title: 'Data board',
                        icon: 'fa fa-tasks',
                       
                    },
                    {
                        title: 'Graph',
                        icon: 'fa fa-chart-area',
                        child: [
                            {
                                href: '/graph',
                                title: 'null',
                                icon: 'fa fa-file-alt'
                            },
                            {
                                href: '/timeserie',
                                title: 'Time Series',
                                icon: 'fa fa-file-alt'
                            },
                            {
                                href: '/horizongraph',
                                title: 'Horizon Graph',
                                icon: 'fa fa-file-alt'
                            }
                        ]
                    }
                ],
                selectedTheme:'white-theme',
                collapsed: false
            }
    },
    
    
    methods: {
        onCollapse (collapsed) {
            console.log(collapsed);
            this.collapsed = collapsed;
        }

    }
  
}
</script>


<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600');

html {
  margin: 0;
  padding: 0;
}
body{
    background-color: #f2f4f7;
}
#demo {
  padding-left: 300px;
}
#demo.collapsed {
  padding-left: 50px;
}
.demo {
  padding: 50px;
}

.container {
  max-width: 90vw;
}

</style>