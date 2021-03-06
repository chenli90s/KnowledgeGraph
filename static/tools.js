const prefix = 'image://';


class GragChart {

    constructor(chart) {
        this.app = echarts.init(chart)
        this.cass = [{name: 'ups'}, {name: 'downs'}, {name: '合成路线'}];
        this.app.on('mouseup', function (params) {
            // console.log(params)
            let option = app.getOption();
            option.series[0].data[params.dataIndex].x = params.event.offsetX;
            option.series[0].data[params.dataIndex].y = params.event.offsetY;
            option.series[0].data[params.dataIndex].fixed = true;
            app.setOption(option);
        });
    }


    loadingData(data, cas, key = []) {

        this.keys = key;
        let nodes = [];
        let links = [];
        this.cass = this.cass.unshift({name: cas})

        function genEleNode(v, cate) {
            if (key.indexOf(v.cas) < 0) {
                let symbol = v.url ? prefix + v.url : 'rect';
                nodes.push({
                    name: v.cas,
                    id: v.cas,
                    symbol,
                    category: cate,
                    symbolSize: 50,
                    label: {normal: {show: true}}
                })
                // nodes.push({name: v.cas, id: v.cas, category: cate, symbolSize: 30, label: {normal: {show: true}}})
                key.push(v.cas)
            }
        }

        genEleNode(data.info, 0)

        function loadingNodes() {
            data.synts.forEach((val, index) => {
                let mid = val.pre + ":" + Math.random().toString(36).substr(2);
                // var cate = cass.push(`路线${index.toString()}`)
                nodes.push({
                    name: mid,
                    id: mid,
                    value: val.pre,
                    category: 3,
                    symbolSize: 15,
                    symbol: 'diamond',
                    label: {normal: {show: false}}
                })
                val.front.forEach(v => {
                    genEleNode(v, 3)
                    links.push({name: null, source: v.cas, target: mid, value: '构成', lineStyle: {normal: {}}})
                });
                val.back.forEach(v => {
                    genEleNode(v, 3)
                    links.push({name: null, source: mid, target: v.cas, value: '转化', lineStyle: {normal: {}}})
                })
            });
        }

        function loadingupdown(data, cas) {
            data.updown.ups.forEach(val => {
                genEleNode(val, 1);
                links.push({name: null, source: cas, target: val.cas, value: '上游', lineStyle: {normal: {}}})
            });
            data.updown.downs.forEach(val => {
                genEleNode(val, 2);
                links.push({name: null, source: cas, target: val.cas, value: '下游', lineStyle: {normal: {}}})
            });
        }

        loadingNodes();
        loadingupdown(data, cas)

        return {nodes, links};
    }


    gen_synt(data, key = []) {
        this.keys = key
        let nodes = [];
        let links = [];

        function genEleNode(v, cate) {
            if (key.indexOf(v.cas) < 0) {
                let symbol = v.url ? prefix + v.url : 'rect';
                nodes.push({
                    name: v.cas,
                    id: v.cas,
                    symbol,
                    category: cate,
                    symbolSize: 50,
                    label: {normal: {show: true}}
                })
                // nodes.push({name: v.cas, id: v.cas, category: cate, symbolSize: 30, label: {normal: {show: true}}})
                key.push(v.cas)
            }
        }

        function loadingNodes() {
            data.synts.forEach((val, index) => {
                let mid = val.pre + ":" + Math.random().toString(36).substr(2);
                // var cate = cass.push(`路线${index.toString()}`)
                nodes.push({
                    name: mid,
                    id: mid,
                    value: val.pre,
                    category: 3,
                    symbolSize: 15,
                    symbol: 'diamond',
                    label: {normal: {show: false}}
                })
                val.front.forEach(v => {
                    genEleNode(v, 3)
                    links.push({name: null, source: v.cas, target: mid, value: '构成', lineStyle: {normal: {}}})
                });
                val.back.forEach(v => {
                    genEleNode(v, 3)
                    links.push({name: null, source: mid, target: v.cas, value: '转化', lineStyle: {normal: {}}})
                })
            });
        }

        loadingNodes()
        return {nodes, links}
    }


    gen_updowns(data, cas, updown, key = []) {
        this.keys = key;
        let nodes = [];
        let links = [];

        function genEleNodes(v, cate) {
            if (key.indexOf(v.cas) < 0) {
                let symbol = v.url ? prefix + v.url : 'rect';
                nodes.push({
                    name: v.cas,
                    id: v.cas,
                    symbol,
                    category: cate,
                    symbolSize: 50,
                    label: {normal: {show: true}}
                })
                // nodes.push({name: v.cas, id: v.cas, category: cate, symbolSize: 30, label: {normal: {show: true}}})
                key.push(v.cas)
            }
        }

        // console.log(data.info.cas)
        genEleNodes(data.info, 0)
        data.updown[updown].forEach(val => {
            genEleNodes(val, 2);
            links.push({name: null, source: cas, target: val.cas, value: '下游', lineStyle: {normal: {}}})
        });
        return {nodes, links}
    }

    option(categories, graph) {
        // let height = window.innerHeight
        // let width = window.innerWidth
        nodes.map(n => {
            // n.draggable = true;
            // n.x = Math.random()*width
            // n.y = Math.random()*height
            n.x = n.y = null
        })
        return {
            title: {
                text: '',
                subtext: 'Default layout',
                top: 'bottom',
                left: 'right'
            },
            tooltip: {
                show: false
            },
            legend: [{
                // selectedMode: 'single',
                // data: categories.map(function (a) {
                //     return a.name;
                // })
            }],
            animationDuration: 1,
            animationEasingUpdate: 'quinticInOut',
            series: [
                {
                    name: 'Les Miserables',
                    type: 'graph',
                    layout: 'force',
                    // layout: 'none',
                    data: graph.nodes,
                    links: graph.links,
                    categories: categories,
                    roam: true,
                    focusNodeAdjacency: true,
                    draggable: true,
                    symbolRotate: 2,
                    itemStyle: {
                        normal: {
                            borderColor: '#fff',
                            borderWidth: 2,
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.3)'
                        }
                    },
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [1, 10],
                    edgeLabel: {
                        normal: {
                            textStyle: {
                                fontSize: 12
                            }
                        }
                    },
                    force: {
                        edgeLength: 50,
                        repulsion: 500,
                        layoutAnimation: false
                    },
                    label: {
                        position: 'right',
                        formatter: '{b}'
                    },
                    lineStyle: {
                        color: 'source',
                        // curveness: 0.3,
                        width: 1
                    },
                    emphasis: {
                        lineStyle: {
                            width: 3
                        }
                    },
                    markPoint: {
                        silent: true,
                    },
                    markLine: {
                        silent: true,
                    },
                    markArea: {
                        silent: true,
                    },
                    zlevel: 100,
                },

            ]
        };
    }


    showRelaData(data){
        // this.keys = key;
        // let nodes = [];
        // let links = [];
        this.cass = [{name: data.type}]
        this.show(data)
    }

    show(d, merge = false) {
        // var d = {nodes, links};
        console.log(d);
        options = option(cass, d);
        // options.series[0].fixed = false;
        app.setOption(options, merge);
        options.series[0].fixed = true;
        setTimeout(() => {
            app.setOption(options)
        }, 1000);
        window.onresize = () => {
            app.setOption(options)
        }

    }

}


