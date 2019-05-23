<template>
    <div>
        <div id="graph">
        </div>
        
    </div>
</template>

<script>
export default {
    name: 'StackedBar',
    data: function() {
        return {
           
        }
    }, 
    methods: {
        init(){
            var margin = {top: 60, right: 30, bottom: 30, left: 80},
                width = this.$el.clientWidth*0.95 - margin.left - margin.right,
                height =  300- margin.top - margin.bottom;
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
            
            let x =  d3.scaleLinear().range([0, width]).domain([0, 100]);
            let y =  d3.scaleLinear().range([height,0]).domain([-0.4, 0.4]);
          
            svg.append("g")
                .attr("transform", "translate(0," + (height/2) + ")")
                .call(d3.axisBottom(x).ticks(5));
            svg.append("g")
                .call(d3.axisLeft(y).ticks(5));

            let color = d3.scaleOrdinal()
                .domain(keys)
                .range(['#00E396','#FEB019','#FF4560','#775DD0'])

            title="abc"
            svg.append("text")
                .attr("x", (width / 2))             
                .attr("y", 0 - (margin.top / 4))
                .attr("text-anchor", "middle")  
                .style("font-size", "16px") 
                .text(title);
        }
    }
};
</script>

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