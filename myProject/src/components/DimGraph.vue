<template>
<div>
    <select @change="Onchange($event)" v-model="selected">
            <option v-for="t in types" v-bind:value="t.id">{{t.name}}</option>
    </select>
    <div style="display:flex">
        <div id='dimgraph' style="width:25%"></div>
        <div style="width:5%"></div>
        <div ref="DimPageContainer" style="width:70%"></div> 
    </div>
    <VueSlideBar
      v-model="slider.value"
      :data="slider.data"
      :range="slider.range"
      :labelStyles="{ color: '#4a4a4a', backgroundColor: '#4a4a4a' }"
      :processStyle="{ backgroundColor: '#d8d8d8' }"
      @callbackRange="callbackRange"
      style="width:28%"
      >
      <template slot="tooltip" slot-scope="tooltip">
        <img src="static/images/rectangle-slider.svg">
      </template>
    </VueSlideBar>
</div>
</template>


<script>
import VueSlideBar from 'vue-slide-bar'
import Vue from 'vue'
import HorizonGraph from './HorizonGraph'
export default {
    name: 'DimGraph',
    data: function() {
        return{
           rangeValue: {},
           tags:[],
           types:[],
           selected:"?",
           selectIdx:-1,
           slider: {
                value: 10,
                data: [
                ],
                range: [
                
                ]
            },
            imgUrl1:0,
            imagUrl2:0,
            factor:11,
            instances:[]
        }
    },
    components: {
        VueSlideBar,
        HorizonGraph
    },
    mounted(){
        var self=this;
       
        var tmp=Vue.extend(HorizonGraph)
        var instance=new tmp();
        instance.$mount();
        self.$refs.DimPageContainer.appendChild(instance.$el);     
        //instance.init(self.dataDiff,self.len,self.dim,self.tags);
        self.instances.push(instance);
        instance.paddingLeft="3%";


        this.$axios.get('http://140.113.210.24:5000/dimselect',{responseType: 'blob',params:{dim:-1,factor:self.factor}}).then((response) => {
                var reader = new window.FileReader();
                let imgUrl = URL.createObjectURL(response.data);
                //imageNode.src = imgUrl;
                self.imgUrl1=imgUrl;
                self.draw(imgUrl,null)
            
        });
    
        this.$axios.get('http://140.113.210.24:5000/tags').then((response) => {
            self.tags=response.data['tags']; 
            let i=0;
            for(i;i<self.tags.length;i++)
            {
               self.types.push(
                 {
                   id:i,
                   name:self.tags[i]
                 })
            }
        });
        let i=-50;
        for(i;i<=50;i+=10){
            self.slider.data.push(i);
            self.slider.range.push({label:i});
        }
        window.addEventListener('resize',function () {
            self.removeAll();
            self.draw(self.imgUrl1,self.imgUrl2);
        })
        
    },
    methods: {
        draw(imgUrl1,imgUrl2){
         
            window.d3=d3v4;

            let width = document.getElementById('dimgraph').offsetWidth;

            let svg=d3.select('#dimgraph').append('svg')
                        .attr('width',"100%")
                        .attr('height',"100%")
                svg.append('image')
                    .attr('width','100%')
                    .attr('height','100%')
                    .attr("xlink:href",imgUrl1)
                    .style('border','1px solid black')     
            
            /*
            let svg1=d3.select('#dimgraph').append('svg')
                        .attr('width',width*0.45)
                        .attr('height',width*0.4)
                svg1.append('image')
                    .attr('width','100%')
                    .attr('height','100%')
                    .attr("xlink:href",imgUrl2)
                    .style('border','1px solid black')     
            */
        },
        dropdownUpdate(payload)
        {
            this.object = payload;
        },
        Onchange(event){
            let self=this;
            let index=event.target.value;
            this.selectIdx=index;
            this.update()
                //var d=(response.data['r'])(function(value,index){return value[0]});      
        },
        callbackRange (val) {
            this.rangeValue = val;
            this.factor=parseFloat(val.label)/10+10;
            if(this.selectIdx!=-1)
                this.update();
        },
        removeAll()
        {
            d3.select("#dimgraph").selectAll("svg").remove();
        },
        update()
        {
            let self=this;
            this.$axios.get('http://140.113.210.24:5000/dimselect',{responseType: 'blob',params:{dim:self.selectIdx,factor:self.factor}}).then((response) => {
                var reader = new window.FileReader();
                let imgUrl = URL.createObjectURL(response.data);
                //imageNode.src = imgUrl;
                self.imgUrl1=imgUrl;
                self.removeAll();
                self.draw(self.imgUrl1,self.imgUrl2);
            
            });

            if(self.selectIdx!=-1){
                this.$axios.get('http://140.113.210.24:5000/dimselectDetail',{responseType: 'blob',params:{dim:self.selectIdx,factor:self.factor}}).then((response) => {
                    var reader = new window.FileReader();
                    let imgUrl = URL.createObjectURL(response.data);
                    //imageNode.src = imgUrl;
                    self.imgUrl2=imgUrl;
                    //self.removeAll();
                    //self.draw(self.imgUrl1,self.imgUrl2);
                });
            }
            this.updateHorizonGraph();
        },
        updateHorizonGraph()
        {
            let self=this;
            this.$axios.get('http://140.113.210.24:5000/dimselectDetailData',{params:{dim:self.selectIdx,factor:self.factor}}).then((response) => {
                console.log('a')
                let data=response.data['data'];
                this.instances[0].updateData(data);
            });
            
        }

   }
}
</script>
