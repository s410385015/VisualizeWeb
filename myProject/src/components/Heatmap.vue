<template>
  <div id="heat">
    <apexchart type=heatmap width="95%" height=350 :options=" heatmapOptions" :series="series" />
  </div>
</template>

<script>
import { isObjectExpression } from '@babel/types';
export default {
    name: 'TimeSeries',
    data: function() {
        return{
            heatmapOptions: {
                dataLabels: {
                    enabled: false
                },
                colors: ["#DC143C"],

                title: {
                    text: 'HeatMap Chart'
                }
            },
            series: [{
                name: 'Metric1',
                data: this.generateData(100, {
                min: 0,
                max: 1
                })
            }],
            dataDiff:[],
            len:0,
            dim:0,
            tags:[]
        }
    },
    mounted(){
        let self=this;
     
        this.$axios.get('http://127.0.0.1:5000/reconstructDiff').then((response) => {
            self.dataDiff.push(response.data['r2']);
            self.dataDiff.push(response.data['r4']);
            self.dataDiff.push(response.data['r6']);
            self.dataDiff.push(response.data['r8']);
            self.len=response.data['len'];
            self.dim=response.data['dim'];
            self.tags=response.data['tags'];

           
            self.series=self.generateData(2,self);
            
        });
    },

    methods: {

        generateData(r,self) {
            let idx=0;
            let series=[]
           
            for(idx;idx<self.dim;idx++)
            {
                series.push(
                    {
                        name: self.tags[idx],
                        data: (self.dataDiff[r]).map(value=>value[idx].toFixed(2)),
                        min:0,
                        max:0.3
                    }
                )
            }
            return series;
        }
    }

 
}
</script>


