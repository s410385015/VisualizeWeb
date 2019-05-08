<template>
  <div id="graph">
    <Heatmap/>

    <div class="timeGraph">
      <apexchart width="94%" height="350" type="line" :options="chartOptions" :series="series"></apexchart>
      <select @change="Onchange($event)" v-model="selected">
          <option v-for="t in types" v-bind:value="t.id">{{t.name}}</option>
      </select>
      <input type="checkbox" id="r2_c" value=2 v-model="checkValue" v-on:change="Update()">
      <label for="r2_c">Dim2</label>
      <input type="checkbox" id="r4_c" value=4 v-model="checkValue" v-on:change="Update()">
      <label for="r4_c">Dim4</label>
      <input type="checkbox" id="r6_c" value=6 v-model="checkValue" v-on:change="Update()">
      <label for="r6_c">Dim6</label>
      <input type="checkbox" id="r8_c" value=8 v-model="checkValue" v-on:change="Update()">
      <label for="r8_c">Dim8</label>
    </div>
    <!--<button type="button" @click="test">按鈕要大</button>-->
  </div>
</template>

<script>
import { isObjectExpression } from '@babel/types';
import Heatmap from './Heatmap'

export default {
  name: 'TimeSeries',
  components: {
      Heatmap
  },
  data: function() {
    return {
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
      selected:"?"
    }
  },
  mounted () {
        let _self=this;
        this.$axios.get('http://127.0.0.1:5000/reconstructRaw').then((response) => {
            _self.r=_self.RoundFloat(2,response.data['r']);
            _self.d2=_self.RoundFloat(2,response.data['d2']);
            _self.d4=_self.RoundFloat(2,response.data['d4']);
            _self.d6=_self.RoundFloat(2,response.data['d6']);
            _self.d8=_self.RoundFloat(2,response.data['d8']);
            let x=0;
            let len=_self.r.length;
            let xaxis=[];
            while(x<len)
            {
                xaxis.push(x);
                x++;
            }
            _self.chartOptions.categories=xaxis;
        });
        this.$axios.get('http://127.0.0.1:5000/getraw20').then((response) => {
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
        })
    
        
  },
  methods: {
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
                name: 'r2',
                data: _d2
            },
            {
                name: 'r4',
                data: _d4
            },
            {
                name: 'r6',
                data: _d6
            },
            {
                name: 'r8',
                data: _d8
            },
            
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
   padding-left: 3%;
}
</style>