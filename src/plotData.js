// import {inject} from 'aurelia-framework';
// import {EventAggregator} from "aurelia-event-aggregator";

// @inject(EventAggregator)
// export class PlotData{
// 	constructor(eventAggregator){
// 		// this.pltly = pltly;
// 		this.eventAggregator = eventAggregator;
// 		this.plotData = {};
		
// 		this.eventAggregator.subscribe('plotData', plotData => {
// 													this.plotData= originData; 
// 													console.log(this);
// 												});
// 		// console.log(this.originData);
// 	}
// 	//Stringify data
// 	getData(){
// 		return JSON.stringify(this.plotData);
// 	}
// } 