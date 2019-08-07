<template>
  <div>
    <div id="horizongraph"></div>
  </div>
</template>


<script>
//import _d3 from "../../static/d3.v3.5.5"
//import {cubism} from "../../static/cubism.js"


export default {
    name: 'HorizonGraph',
    data: function() {
        return{
            dataDiff:[],
            len:0,
            dim:0,
            tags:[],
            svg:0,
            colors:[],
            mainData:0,
            co:[],
            date:[],
            raw:[],
            visible:true,
            paddingLeft:"4.5%"
        }
    },
    mounted(){

        
        let self=this;
        
        
        this.$axios.get('http://140.113.210.24:5000/horizongraph').then((response) => {
            self.dataDiff.push(response.data['r2']);
            self.dataDiff.push(response.data['r4']);
            self.dataDiff.push(response.data['r6']);
            self.dataDiff.push(response.data['r8']);
            self.raw=response.data['raw'];
            self.len=response.data['len'];
            self.dim=response.data['dim'];
            self.tags=response.data['tags'];
            self.date=response.data['date'];
      
            self.mainData=self.dataDiff[0];
            let i;
            for(i=0;i<self.dim;i++){
              self.colors.push('#000');
              self.co.push('');
            }
            //self.dataDiff=self.dataDiff[0];
            
       
            self.draw(self.date,self.mainData,self.tags);
            
            
        });
        

        window.addEventListener('resize',function () {
            self.removeAll();
            self.draw(self.date,self.mainData,self.tags);
        })
    
        
    },
    methods: {
        init(date,dataDiff,len,dim,tags)
        {
            this.dataDiff=dataDiff;
            this.len=len;
            this.dim=dim;
            this.tags=tags;
            this.date=date;
            this.mainData=this.dataDiff[0];
            let i;
            for(i=0;i<this.dim;i++){
              this.colors.push('#000');
              this.co.push('');
            }
            //self.dataDiff=self.dataDiff[0];
            this.draw(this.date,this.mainData,this.tags);
        },
        draw(date,data,tags){
            this.removeAll();

            let offset=0.06;
            window.d3=d3v3;
            let self=this;
            tags=tags.map(function(t,i){
                let costr= self.co[i]==''? '' :" ("+self.co[i].toFixed(2)+")";
                return t+costr;
            })


            let width = document.getElementById('horizongraph').offsetWidth;

            let smoothen = 1;

            let time = _.map(date,function(d){return new Date(d);});
            

          
            let context = cubism.context()
                                .serverDelay(new Date(1972,1,1)) //correct sign so axis is correct & not in future.
                                .step(60 * 60 * 24 * 1000 *(data.length/(width*0.94)))
                                .size(width*0.94)
                                .stop();
           
            d3.select("#horizongraph").append("div")
                  .attr("class", "rule")
                  .call(context.rule());
            
            d3.select("#horizongraph").selectAll(".rule").style("padding-left",this.paddingLeft);
            
            d3.select("#horizongraph").selectAll(".axis")
                .data(["bottom"])
                .enter().append("div")
                .attr("class", function(d) { return d + " axis"; })
                .each(function(d) { d3.select(this).call(context.axis(width*offset).ticks(12).orient(d)); });

         
            
          
          
            context.on("focus", function(i) {
              
                if(i>0){               
                  if (i > width-width*offset*2) {
                
                      d3.selectAll(".value").style({
                          "left":  i == null ? null: ((i)+width*offset*0.5) + "px"
                      });
                  } else {
                     
                      d3.selectAll(".value").style({
                          "left": i == null ? null:((i)+(width*offset)) + "px"
                      });
                  }
                }else{
                  
                      d3.selectAll(".value").style({
                          "left": null,
                         
                      });
                }
                

            });
        
        
        

            data = _.map(d3.range(tags.length), function(value) {
                return _.map(d3.range(data.length), function(idx) { 
                    return data[idx][value];
                })
            });
    

            function metric(name, values) {
                var num = context.size();
                return context.metric(function(start, stop, step, callback) {
                    var data = _.map(d3.range(num), function(d) {
					            	var value ;
                        var idxCalculated = values.length / num * d;
                        var idx = Math.floor(idxCalculated);
                        if (d > 0) {
                            var i = d3.interpolateNumber(values[idx-1], values[idx]);
                            value = smoothen ? i(idxCalculated % 1) : values[idx] 
                        }

                        return value;
                    })
                    callback(null, data);
                }, name);
            };
            
        

            var metrics = _.map(data, function(d, i) {
                return metric(tags[i], data[i]);
            });
        
          

            d3.select("#horizongraph").selectAll(".horizon").data(metrics)
                .enter().insert("div", ".bottom")
                .attr("class", "horizon")
                .call(context.horizon(width*offset)
                .mode("mirror")
                .colors(["#E06C4C", "#EBA18F", "#F5D2CA", "#C0E2F0", "#7AC4E0", "#1DA4D1"].reverse())
                //.colors(["#0000D4","#A8A8FF","#4C4CFF","#FFB0B0","#FF5050","#FF0404"])
                .format(d3.format(".2f")));   

          
            //d3.select("#horizongraph").selectAll(".rule").style("padding-left","6%");
            d3.select("#horizongraph").selectAll(".horizon").select('.title').style("color", function(d, i) {
                  return self.colors[i];
            });
            
            d3.select("#horizongraph").selectAll(".horizon").on('click',function(ctx,idx)
            {

                let IndexInfo=self.calculateIdx(self.raw,idx);
                let newIndex=IndexInfo.map(function(a){ return a.index});
                self.colors=IndexInfo.map(function(a){ return a.color});

                self.reorder(newIndex);
                
                d3.select("#horizongraph").selectAll(".horizon").remove();
                self.removeAll()
                self.draw(self.date,self.mainData,self.tags);
                /*
                d3.selectAll('.horizon').select('.title').style("color", function(d, i) {
                    if(i!=idx)
                      return "#ff0000";
                });
                */
            });

              
       
      
        },
        removeAll(){
            d3.select("#horizongraph").selectAll(".axis").remove();
            d3.select("#horizongraph").selectAll(".horizon").remove();
            d3.select("#horizongraph").selectAll(".rule").remove();
            this.tags=this.tags.map(function(tag){
                return (tag.split(' '))[0]
            })
        },
        reorder(idx){
            let self=this;
            this.mainData= this.mainData.map(function(row){
                return row.map(function(e,i){
                    return row[idx[i]];
                })
            })
          
            this.tags=this.tags.map(function(tag,i){   
                return self.tags[idx[i]];
            })
            this.co=this.co.map(function(c,i){
                return self.co[idx[i]];
            })
          
        },
        corr(d1, d2) {
            let { min, pow, sqrt } = Math
            let add = (a, b) => a + b
            let n = min(d1.length, d2.length)
            if (n === 0) {
              return 0
            }
            [d1, d2] = [d1.slice(0, n), d2.slice(0, n)]
            let [sum1, sum2] = [d1, d2].map(l => l.reduce(add))
            let [pow1, pow2] = [d1, d2].map(l => l.reduce((a, b) => a + pow(b, 2), 0))
            let mulSum = d1.map((n, i) => n * d2[i]).reduce(add)
            let dense = sqrt((pow1 - pow(sum1, 2) / n) * (pow2 - pow(sum2, 2) / n))
            if (dense === 0) {
              return 0
            }
            return (mulSum - (sum1 * sum2 / n)) / dense
        },
        calculateIdx(data,idx){

            
            let co=[];
            let i;
            let keyData=data.map(function(row){
                return row[idx];
            });

            this.co=[];
            for(i=0;i<this.dim;i++)
            {
                let d=data.map(function(row){
                    return row[i];
                });
                let c=this.corr(keyData,d);
                
                this.co.push(c)
                c= c>0 ? (1-c): (-1.1-c);
                let clr= (c==0)? '#000' : ((c>0) ? '#f00':'#00f');

                co.push({index:i,value:c,color:clr});
            }

            

            co.sort(function(a,b){
                return b.value-a.value;
            })
          

            return co;
        },
        updateData(data)
        {

            this.mainData=data;
            this.removeAll();
            this.draw(this.date,this.mainData,this.tags);
        },
        setVisible(flag)
        {
        
          this.visible=flag;
           
        },
        getstyle(sname) {
          for (var i=0;i<document.styleSheets.length;i++) {
            var rules;
            if (document.styleSheets[i].cssRules) {
              rules = document.styleSheets[i].cssRules;
            } else {
              rules = document.styleSheets[i].rules;
            }
            for (var j=0;j<rules.length;j++) {
              if (rules[j].selectorText == sname) {
                return rules[j].style;
              }
            }
          }
        }



   }
}
</script>


<style>

body {
  font-family: 'Lucida Grande', 'Lucida Sans Unicode', Arial, Helvetica, "Helvetica Neue", Helvetica, sans-serif;
  margin: 30px auto;
  width: 100%;
  position: relative;
}

header {
  padding: 6px 0;
}

.group {
  margin-top: 1em;
}

.axis {
  
  font: 10px sans-serif;
  position: fixed;
  pointer-events: none;
  z-index: 2;
}

.axis text {

  -webkit-transition: fill-opacity 250ms linear;
  font-family: 'Lucida Grande', 'Lucida Sans Unicode', Arial, Helvetica, "Helvetica Neue", Helvetica, sans-serif;
}

.axis path {

  display: none;
}

.axis line {

  stroke: #000;
  shape-rendering: crispEdges;
}

.axis.top {
  
  background-image: linear-gradient(top, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -o-linear-gradient(top, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -moz-linear-gradient(top, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -webkit-linear-gradient(top, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -ms-linear-gradient(top, #fff 0%, rgba(255,255,255,0) 100%);
  top: 0px;
  padding: 0 0 24px 0;
}

.axis.bottom {
  background-image: linear-gradient(bottom, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -o-linear-gradient(bottom, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -moz-linear-gradient(bottom, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -webkit-linear-gradient(bottom, #fff 0%, rgba(255,255,255,0) 100%);
  background-image: -ms-linear-gradient(bottom, #fff 0%, rgba(255,255,255,0) 100%);
  bottom: 0px;
  width:94%;
  padding-left: 1.5%;
}

.horizon {
  
  padding-left: 6%;
  /*border-bottom: solid 1px #000;*/
  overflow: auto;
  position: relative;
}



.horizon {
   
  /*border-top: solid 1px #000;*/
  /*border-bottom: solid 1px #000;*/
}

.horizon + .horizon {
  
  border-top: none;
}

.horizon canvas {
  display: block;
}

.horizon .border,
.horizon .title,
.horizon .value {
  bottom: 0;
  line-height: 30px;
  margin: 0 6px;
  position: absolute;
  text-shadow: 0 1px 0 rgba(255,255,255,.5);
  white-space: nowrap;
  font-size: 12px;
}

.horizon .title {
  left:0;
}

.horizon .value {
  right: 0; 
}

.horizon .border{
  height:30px;
  left: 6%;
  content: ""; /* This is necessary for the pseudo element to work. */ 
  display: block; /* This will put the pseudo element on its own line. */
  margin: 0 auto; /* This will center the border. */
  width: 94%; /* Change this to whatever width you want. */
  border-bottom: solid 1px #000;
}

.horizon .border {
  border-top: solid 1px #000;
}


.horizon ~ .horizon .border{
  border-top: none;
}

.line {
  background: #000;
  z-index: 2;
}

.rule{
  height:100%;
  position: absolute;
  padding-left: 3%; 
}
</style>