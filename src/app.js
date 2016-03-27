export class App {
  configureRouter(config, router) {
    config.title = 'Software Reliability Tool';
    config.map([
      { route: ['', 'welcome'], name: 'welcome',      moduleId: 'welcome',      nav: true, title: 'Welcome' },
      { route: 'about', name:'about', moduleId:'about', nav:true, title: "About"}
    ]);

    this.router = router;
  }
}
