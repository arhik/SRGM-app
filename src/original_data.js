import {inject} from 'aurelia-framework';
import {EventAggregator} from "aurelia-event-aggregator";

@inject(EventAggregator)
export class OriginData{
	constructor(eventAggregator){
		// this.pltly = pltly;
		this.eventAggregator = eventAggregator;
		this.originData = {};
		this.plotData = {};
		this.eventAggregator.subscribe('rawdata', originData => {
													this.originData= originData; 
													// console.log(this);
												});
		this.eventAggregator.subscribe('plotData', plotData => {
													this.plotData= plotData; 
													console.log(this.plotData);
												});
		// console.log(this.originData);
	}
	//Stringify data
	activate(){
	
	}

	getRawData(){
		return JSON.stringify(this.originData);
	}

	getPlotData(){
		return JSON.stringify(this.plotData)
	}
} 