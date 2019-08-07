<template>
        <div id="stackbargraph" style="padding-top: 150px;"></div>
</template>

<script>
window.d3=d3v4;

export default {
    name: 'StackedBar',
    data: function() {
        return {
          keys:[],
          data:[],
          len:0,
          title:'' 
        }
    }, 
    mounted() {
        let self=this;
        window.addEventListener('resize',function () {//执行
            self.removeAll();
            self.draw(self.keys,self.data,self.len,self.title);
            
        })
    
    },
    methods: {
        init(keys,data,len,title){
            this.keys=keys;
            this.data=data;
            this.len=len;
            this.title=title;
            this.draw(keys,data,len,title)

        },
        draw(keys,data,len,title){
            var offset=0.06;

            window.d3=d3v4;
            var margin = {top: 60, right: 30, bottom: 30, left: document.getElementById('stackbargraph').offsetWidth*offset},
                width = document.getElementById('stackbargraph').offsetWidth - margin.left,
                height =  300- margin.top - margin.bottom;
        // let width = document.getElementById('horizongraph').offsetWidth;
       
            var svg=d3.select("#stackbargraph")
                                .append("svg")
                                .attr("width", width+margin.left+margin.right)
                                .attr("height", height + margin.top + margin.bottom)
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
            
      
            svg.append("text")
                .attr("x", (width / 2))             
                .attr("y", 0 - (margin.top / 4))
                .attr("text-anchor", "middle")  
                .style("font-size", "16px") 
                .text(title);
            

        
            
            var stackedData = d3.stack()
                .offset(d3.stackOffsetZero)
                .keys(keys)
                (data)
        
            
            let groups=svg
                .selectAll("layer")
                .data(stackedData)
                .enter()
                .append("g")
                .style("fill", function(d,i) { return color(d.key); })
            
            var rect = groups.selectAll("rect")
                .data(function(d) { return d; })
                .enter()
                .append("rect")
                .attr("x", function(d,i) { return x(i); })
                .attr("y", function(d) { 
                    if((d[1]-d[0])>0)
                        return y(d[1]-d[0])
                    else
                        return y(0)
                    
                 })
                .attr("height", function(d) { return Math.abs(y(d[1])-y(d[0])); })
                .attr("width", 8)
                
              
                
          
        },
        removeAll(){
            d3.select("#stackbargraph").select("svg").remove();
        }
    }
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