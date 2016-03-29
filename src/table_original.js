import {inject, customElement} from 'aurelia-framework';
import {EventAggregator} from "aurelia-event-aggregator";
@customElement("table-original")
@inject(EventAggregator)
export class TableOrigData{
	constructor(eventAggregator){
		// this.pltly = pltly;
		this.eventAggregator = eventAggregator;
		this.tableData = {"x":[1,2,3,3,4,5,6,67,7,8,8,9,9,1],"y":[23,3,54,5,3,32,34,5,5,63234,65,3]};
		this.tableheader = Object.keys(this.tableData);
		// console.log(this.originData);
	}
	//Stringify data
	attached(){
		this.eventAggregator.subscribe('rawdata', originData => {
													this.tableData= originData; 
													console.log("table data")
													console.log(this.tableheader)
													console.log(this.tableData)
													this.tableheader = Object.keys(this.tableData);
													console.log(this.tableheader)
													console.log("hello")
													console.log(this);
												});
	}

	getData(){
		return JSON.stringify(this.tableData);
	}
} 