import {customElement, inject, bindable, TaskQueue} from 'aurelia-framework';
import {EventAggregator} from "aurelia-event-aggregator";
import Plotly from 'plotly.js' //It is an issue for now: https://github.com/plotly/plotly.js/issues/22 
// import OriginData from './original_data';
import $ from "jquery";
@customElement('plotest')
@inject(EventAggregator, TaskQueue)
export class Plotest{
	@bindable plotlydiv;
	constructor(eventAggregator, taskQueue){
		this.eventAggregator = eventAggregator;
		this.taskQueue = taskQueue;
		this.plotData = {};
	}

	attached(){
		var layout = {
			title:"Mean Value Function Plot",
			  autosize: false,
			  height:400,
			  width:500,
			  margin: {
			    l: 50,
			    r: 50,
			    b: 50,
			    t: 50,
			    pad: 2
			  }
			};
		var TESTER = this.plotlydiv;
		console.log(TESTER);
		this.taskQueue.queueMicroTask(() => {
			this.eventAggregator.subscribe('plotData', plotdata => {
														this.plotData= plotdata; 
														console.log(this);
														console.log("plotlyData is triggered");
														console.log(this.plotData.plotlyPlot);
														this.plotlydiv.data.push(this.plotData.plotlyPlot);
														// this.plotlydiv.
														// Plotly.plot(this.plotlydiv, this.plotData.plotlyPlot,layout);
														Plotly.redraw(this.plotlydiv)
														this.plotlydiv.on('plotly_selected',function(eventData){
				// console.log(eventData.points);
					if(eventData!==undefined){
						console.log(eventData.points)
						// return eventData.points;
						
					}
					else{

					}
				})
			});	
			
		});
		this.taskQueue.queueMicroTask(() => {
			this.eventAggregator.subscribe('rawdata', rawdata => {
														this.rawData= rawdata; 
														console.log(this);
														// console.log(Plotly);
														// console.log(this.plotData);
														Plotly.plot(this.plotlydiv, this.rawData,layout);
														this.plotlydiv.on('plotly_selected',function(eventData){
				// console.log(eventData.points);
					if(eventData!==undefined){
						console.log(eventData.points)
						// return eventData.points;
					}
					else{

					}
				})
			});	
			
		});

		// this.taskQueue.queueMicroTask(() => {
		// 	this.eventAggregator.subscribe('plotData', plottdata => {
		// 												this.plottingData= plottdata; 
		// 												"plotest plotData is triggered here is the proof"
		// 												console.log(this);
		// 												// console.log(Plotly);
		// 												// console.log(this.plotData);
		// 												Plotly.plot(this.plotlydiv, this.plottingData.plotlyPlot,layout);
		// 												this.plotlydiv.on('plotly_selected',function(eventData){
		// 			// console.log(eventData.points);
		// 			if(eventData!==undefined){
		// 				console.log(eventData.points)
		// 				// return eventData.points;
						
		// 			}
		// 			else{

		// 			}
		// 		})
		// 	});
		// });
		
	}
} 