<template>
  <div id="graph">
    <!--<Heatmap/>-->
    
    
    <div class="timeGraph">
        <select @change="Onchange($event)" v-model="selected">
            <option v-for="t in types" v-bind:value="t.id">{{t.name}}</option>
        </select>
        <apexchart width="98%" left="6.5%" height="250" type="line"  :options="chartOptions" :series="series"></apexchart>  
      
        <!--
        <input type="checkbox" id="r2_c" value=2 v-model="checkValue" v-on:change="Update()">
        <label for="r2_c">Dim2</label>
        <input type="checkbox" id="r4_c" value=4 v-model="checkValue" v-on:change="Update()">
        <label for="r4_c">Dim4</label>
        <input type="checkbox" id="r6_c" value=6 v-model="checkValue" v-on:change="Update()">
        <label for="r6_c">Dim6</label>
        <input type="checkbox" id="r8_c" value=8 v-model="checkValue" v-on:change="Update()">
        <label for="r8_c">Dim8</label>-->
    </div>
    
    <div ref="containerGraph"></div> 
    <!--<div ref="container" ></div>-->
    <!--<button v-on:click="ModeSwitch">{{BtnMsg}}</button>-->
    <!--
    <div v-if="mode">
        <VueSlideBar
          v-model="value2"
          :min="1"
          :max="10"
          :processStyle="slider.processStyle"
          :lineHeight="slider.lineHeight"
          :tooltipStyles="{ backgroundColor: 'red', borderColor: 'red' }">
        </VueSlideBar>
        <h2>Value: {{value2}}</h2>
           
    </div>
    -->
    <!--<div ref="containerg"></div>-->
    
    <!--<div ref="containerg"></div>-->
   
  
    <!--<button type="button" @click="test">按鈕要大</button>-->
  </div>
</template>

<script>
import { isObjectExpression } from '@babel/types';
import Heatmap from './Heatmap'
import StreamGraph from './StreamGraph'
import StackedBar from './StackedBar'
import Vue from 'vue'
import VueSlideBar from 'vue-slide-bar'
import HorizonGraph from './HorizonGraph'

export default {
  name: 'HorizonGraphPage',
  components: {
      Heatmap,
      StreamGraph,
      StackedBar,
      VueSlideBar,
      HorizonGraph
  },
  data: function() {
    return {
      mode:false,
      BtnMsg: "StackedBar",
      value2: 8,
      slider: {
        lineHeight: 10,
        processStyle: {
          backgroundColor: 'red'
        }
      },
      chartOptions: {
        xaxis: {
          categories:[],
          labels:{
              show:false,
          }
        },
        title: {
            text: '',
            align: 'left'
        },
        stroke: {
            width: [2, 1, 1],
            curve: 'straight',
        },
      },
      series: [],
      r:[],
      d2:[],
      d4:[],
      d6:[],
      d8:[],
      types:[],
      checkValue:["2","4","6","8"],
      selectIdx:-1,
      selected:"?",
      dataDiff:[],
      len:0,
      dim:0,
      tags:[],
      stackData:[],
      keys:[],
      instances:[],
      date:[]
    }
  },
  mounted () {
        let self=this;
     
        var tmp=Vue.extend(HorizonGraph)
        var instance=new tmp();
        instance.$mount();
        self.$refs.containerGraph.appendChild(instance.$el);
        
        //instance.init(self.dataDiff,self.len,self.dim,self.tags);
        self.instances.push(instance);
        
        


        let _self=this;
        this.$axios.get('http://140.113.210.24:5000/linegraph').then((response) => {
            _self.r=_self.RoundFloat(0,response.data['r']);
            _self.d2=_self.RoundFloat(0,response.data['d2']);
            _self.d4=_self.RoundFloat(2,response.data['d4']);
            _self.d6=_self.RoundFloat(2,response.data['d6']);
            _self.d8=_self.RoundFloat(2,response.data['d8']);
            _self.date=response.data['date'].map(function(d){
                return d.substr(0,10);
            })
            
     
            let x=0;
            let len=_self.r.length;
            this.chartOptions={
                xaxis: {
                        categories:_self.date
                }
            }
        });
        this.$axios.get('http://140.113.210.24:5000/getraw20').then((response) => {
            let _r = Object.keys((JSON.parse("["+response.data+"]"))[0]);
            let i=0;
            for(i;i<_r.length;i++)
            {
               _self.types.push(
                 {
                   id:i,
                   name:_r[i]
                 })
            }

          
        });

    
        
        
        this.$axios.get('http://140.113.210.24:5000/reconstructDiffDiv').then((response) => {
            _self.dataDiff.push(response.data['r2']);
            _self.dataDiff.push(response.data['r4']);
            _self.dataDiff.push(response.data['r6']);
            _self.dataDiff.push(response.data['r8']);
            _self.len=response.data['len'];
            _self.dim=response.data['dim'];
            _self.tags=response.data['tags']; 
            let i=0;
            for(i;i<_self.dim;i++)
            {
                let _r2=_self.dataDiff[0].map(value=>value[i])
                let _r4=_self.dataDiff[1].map(value=>value[i])
                let _r6=_self.dataDiff[2].map(value=>value[i])
                let _r8=_self.dataDiff[3].map(value=>value[i])

                let tmpArray=[]

                let j=0;
                for(j;j<_self.len;j++)
                {
                    tmpArray.push({r2:_r2[j],r4:_r4[j],r6:_r6[j],r8:_r8[j]})
                }
                
                _self.stackData.push(tmpArray)
            }


           
            _self.keys=Object.keys(_self.stackData[0][0]);
            
            //this.mode=true;
            //_self.dim=1 
            
            
            for(i=0;i<_self.dim;i++){
                var tmp=Vue.extend(StackedBar)
                var instance=new tmp()
                instance.$mount()
                _self.$refs.containerGraph.appendChild(instance.$el)
               
                instance.init(_self.keys,_self.stackData[i],_self.len,_self.tags[i])
                _self.instances.push(instance)
            }
            
            
            

        });
        
        
        
  },
  methods: {

    
      ModeSwitch(){
          if(this.BtnMsg=="StreamGraph")
          {
              this.BtnMsg="StackedBar";
              this.mode=false;
              
              
          }
          else
          {
              this.BtnMsg="StreamGraph";
              this.mode=true;
             
          }
      },
      test(){
          console.log(this.checkValue.includes('2'))
      },
      Onchange(event){
        let _self=this;
        let _index=event.target.value;
        _self.selectIdx=_index
        _self.Update(_index)
            //var d=(response.data['r'])(function(value,index){return value[0]});      
      },
      Update(){
        
        let _self=this;
        let idx=_self.selectIdx;
        let _r=(_self.r).map(value=>value[idx]);
        let _d2=this.checkValue.includes('2')?(_self.d2).map(value=>value[idx]):[];
        let _d4=this.checkValue.includes('4')?(_self.d4).map(value=>value[idx]):[];
        let _d6=this.checkValue.includes('6')?(_self.d6).map(value=>value[idx]):[];
        let _d8=this.checkValue.includes('8')?(_self.d8).map(value=>value[idx]):[];

  
        //console.log((_self.r).map((value,index)=>{ return value[2]; }))
        let series = [
            {
                name: 'raw',
                //data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {
                data: _r
                
            },
            {
                name: 'reconstruct',
                data: _d2
            }
            
        ]
        _self.series = series;
           
      },

      RoundFloat(p,array){
          let x=0;
          let len=array.length;
          while(x<len){
              let index=0;
              let l=array[x].length;
              while(index<l){
                  array[x][index]=(parseFloat(array[x][index])).toFixed(p);
                  index++;
              }
              x++;
          }
        
          return array;
      },

    
  }
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600');

#graph {
  
}
.timeGraph {
   padding-left: 0%;
}

.apexcharts-canvas {
    padding-left: 2.5%;
}
</style>