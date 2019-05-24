<template>
    <div>
        <div id="graph">
        </div>
        
    </div>
</template>

<script>
//import * as d3 from 'd3';
export default {
    name: 'StreamGraph',
    data: function() {
        return {
      
        }
    },
    mounted() {
        
        //this.init();
        //this.calculatePath();
        //this.init();
    },
    methods: {
    
        init(keys,data,len,title){
            //let svg=d3.select(this.$el).select('svg')
            //let x= d3.scale.linear().domain(d3.extent([1,2,3,4,5]).range([0,800]).range([0,this.width])
            this.draw(keys,data,len,title)
    
        },
        draw(keys,data,len,title){

          
            var margin = {top: 60, right: 30, bottom: 30, left: 80},
                width = this.$el.clientWidth*0.95 - margin.left - margin.right,
                height =  300- margin.top - margin.bottom;

            console.log('?')
            var svg=d3.select("#graph")
                                //.append("div")
                                //.classed("svg-container", true)
                                .append("svg")
                                .attr("width", width+margin.left+margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                //.attr("preserveAspectRatio", "xMinYMin meet")
                                //.attr("viewBox", "0 0 "+(width + margin.left + margin.right)+" "+(height + margin.top + margin.bottom))
                                //.classed("svg-content-responsive", true)
                                .append("g")
                                .attr("transform","translate(" + margin.left + "," + margin.top + ")")
                               
            
            let x =  d3.scaleLinear().range([0, width]).domain([0, len]);
            let y =  d3.scaleLinear().range([height,0]).domain([-0.35, 0.35]);
          
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).ticks(5));
            svg.append("g")
                .call(d3.axisLeft(y));

          
            let color = d3.scaleOrdinal()
                .domain(keys)
                .range(['#00E396','#FEB019','#FF4560','#775DD0'])
            
           //let colors=['#C2F0E4','#FEB019','#FF4560','#775DD0']
            svg.append("text")
                .attr("x", (width / 2))             
                .attr("y", 0 - (margin.top / 4))
                .attr("text-anchor", "middle")  
                .style("font-size", "16px") 
                .text(title);
            

            /*
            let tmp=[]
            let k=0
            for(k;k<keys.length;k++)
                tmp.push([])

            let i=0
            

            let max=-1
            let min=1

            for(i;i<data.length;i++)
            {   
                let j=0
                let _x=[]
                for(j;j<keys.length;j++)
                {
                    let n=0
                    
                    let flag= (data[i][keys[j]]>=0)? true:false
                    
                    if(data[i][keys[j]]>max)
                        max=data[i][keys[j]]
                    if(data[i][keys[j]]<min)
                        min=data[i][keys[j]]

                    let t=0;
                    for(n;n<keys.length;n++)
                    {
                        if(n==j)
                            continue
                        if(flag){
                            if(data[i][keys[n]]>t && data[i][keys[n]]<data[i][keys[j]])
                                t=data[i][keys[n]]
                        }
                        else{
                            if(data[i][keys[n]]<t && data[i][keys[n]]>data[i][keys[j]])
                                t=data[i][keys[n]]
                        }

                    }
                    _x.push([t,data[i][keys[j]]])
                    tmp[j].push([t,data[i][keys[j]]])
                }
                //console.log(i.toString())
                //console.log(_x)
            }
            */
            //co
            //let stackedData=[];

         
            /*
            let stackedData = tmp.reduce(function(result, field, index) {
                    result[keys[index]] = field;
                    return result;
            }, {})
            */
            
            var stackedData = d3.stack()
                .offset(d3.stackOffsetZero)
                .keys(keys)
                (data)
                
            
            svg
                .selectAll("layer")
                .data(stackedData)
                .enter()
                .append("path")
                .attr("opacity", 1)
                .attr("class", "layer")
                .style("fill", function(d,i) { return color(d.key); })
                .attr("d", d3.area()
                    .x(function(d, i) {return x(i); })
                    .y0(function(d) { return y(0); })
                    .y1(function(d) { return y(d[1]-d[0]); })
                )
                .attr("opacity", 1)
                .on("mouseover", function(d, i) {
                    svg.selectAll(".layer").transition()
                    .duration(150)
                    .attr("opacity", function(d, j) {
                        return j != i ? 0.4 : 1;
                })})
                .on("mouseout", function(d, i) {
                    svg.selectAll(".layer")
                    .transition()
                    .duration(250)
                    .attr("opacity", "1");
                })     
                
                
          
        },
        getScales() {
            const x = d3.scaleTime().range([0, this.width]);
            const y = d3.scaleLinear().range([210, 0]);
            d3.axisLeft().scale(x);
            d3.axisBottom().scale(y);
            x.domain(d3.extent(this.data, (d, i) => i));
            y.domain([0, d3.max(this.data, d => d)]);
            return { x, y };
        },
        calculatePath() {
            const scale = this.getScales();
            const path = d3.line()
                .x((d, i) => scale.x(i))
                .y(d => scale.y(d));
            this.line = path(this.data);
            
        },
        removeAll(){
            d3.select("#graph").select("svg").remove()
        }
    },
};
</script>


<style>
.svg-container {
    display: inline-block;
    position: relative;
    width: 95%;
    padding-bottom: 100%; /* aspect ratio */
    vertical-align: top;
    overflow: hidden;
}
.svg-content-responsive {
    display: inline-block;
    position: absolute;
    top: 10px;
    left: 0;
}
</style>