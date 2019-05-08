
<template>
  <div>
    <!-- <input type='file' id='upload' @change="uploadFile"> -->
    <!--<button type="button" @click="prompt">按鈕要大</button>-->
    <div>
          Select Data:
          <select @change="dataSelect">
            <option
              v-for="(data, index) in dataSet"
              :key="index"
            >
              {{ data == '' ? 'null' : data }}
            </option>
          </select>
    </div>
    
    <vuetable ref="vuetable"
    :api-mode="false"
    :fields="fields"
    :data="localdata"
    :per-page="perPage"
    ></vuetable>
  </div>
</template>


<script>
import Vuetable from 'vuetable-2/src/components/Vuetable'
import VuetablePagination from 'vuetable-2/src/components/VuetablePagination'
import DataField from "./DataField.js"
//import EcoFile from "./data.json"
export default {
    components: {
      Vuetable,
      VuetablePagination
    },
    data() {
        return{
            fields:DataField,   
            localdata:[],
            dataSet:['null','eco'],
            rawData:{},
            perPage:10,
        };
    },
    mounted () {
        let _self=this
        this.$axios.get('http://127.0.0.1:5000/getraw20').then((response) => {
            _self.rawData = JSON.parse("["+response.data+"]");
        })
    },
    methods:{
         prompt(){
            this.$axios.get('http://127.0.0.1:5000/getraw20').then((response) => {
             var d='['+response.data+']';
             var newD=JSON.parse(d);
             console.log(Object.keys(newD[0]));
           
         })
         },
         dataSelect: async function(e)
         {
            if(e.target.value=='eco'){
             //console.log(Object.keys(retjson[0]))
             this.AddField(Object.keys(this.rawData[0]));
             this.localdata=this.rawData;
            
            }
             //this.localdata=this.rawData;
            
         },
         AddField(fieldTitle)
         {
            console.log(fieldTitle)
            var ref=this;
            fieldTitle.forEach(function(element) {
                 ref.fields.push({name:element,title:element});
            });
            this.$refs.vuetable.normalizeFields();
         },
        //  readxlsx(inpdata, fmt) {
        //     //讀取xlsx檔

        //     //參數
        //     //inpdata為由input file讀入之data
        //     //fmt為讀取格式，可有"json"或"csv"，csv格式之分欄符號為逗號，分行符號為[\n]

        //     //說明
        //     //所使用函式可參考js-xlsx的GitHub文件[https://github.com/SheetJS/js-xlsx]


        //     //to_csv
        //     function to_csv(workbook) {
        //         var result = [];
        //         workbook.SheetNames.forEach(function(sheetName) {
        //             var csv = XLSX.utils.sheet_to_csv(workbook.Sheets[sheetName]);
        //             if(csv.length > 0){
        //                 result.push('SHEET: ' + sheetName);
        //                 result.push('\n');
        //                 result.push(csv);
        //             }
        //         });
        //         return result;
        //     }

        //     function to_json(workbook) {
        //         var result = {};
        //         workbook.SheetNames.forEach(function (sheetName) {
        //             var roa = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
        //             if (roa.length > 0) {
        //                 result['data'] = roa;
        //             }
        //         });
        //         return result;
        //     }

        //     //讀檔
        //     var workbook = XLSX.read(inpdata, { type: 'binary' });

        //     if (fmt === 'json') {
        //         return to_json(workbook);
        //     }
        //     else {
        //         return to_csv(workbook);
        //     }

        // },
        // LoadFile(f)
        // {
                
        //     var reader = new FileReader();

        //         //檔案名稱
        //     var name = f.name;
        //     var ref=this;
            
     
        //         //onload觸發事件
        //     reader.onload = function (e) {

        //         //對象內資料
        //         var data = e.target.result;
                
        //         //讀取xlsx資料
        //         //var retcsv = ref.readxlsx(data, 'csv');
        //         var retjson=ref.readxlsx(data,'json');
        //         //var matadata=retcsv[2].split('\n');
        //         //var fieldTitle=matadata[0].split(',');
        //         //ref.localData=retjson;
        //         ref.AddField(Object.keys(retjson['data'][0]));
        //         ref.localdata=retjson;
        //         //顯示內容
                                    
        //     };
           
        //     reader.readAsBinaryString(f);
        // },
        // uploadFile(event){


        //     var files = event.target.files;
        //     var f = files[0]; 
        //     console.log(typeof(f));
            
        //     var ref=this;
        //     var oReq = new XMLHttpRequest();
        //     oReq.open("GET", "./components/a.txt",true);
        //     oReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        //     //oReq.responseType = 'blob';
        //     //oReq.responseType = 'blob';
        //     //var ref=this;
        //     oReq.onload = function () {    
        //         if(oReq.readyState==4&&oReq.status==200){

        //         }
        //         //ref.LoadFile(this.response); 
        //     //    ref.LoadFile(oReq.response);
        //     };
        //     oReq.send();
            
        //     //var files = event.target.files;
        //     //var f = files[0]; 
        //     //this.LoadFile(f);
        // },
       
        
       

    }
    //...
  }
</script>