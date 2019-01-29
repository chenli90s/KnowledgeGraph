function option(categories, graph) {
    let height = window.innerHeight
    let width = window.innerWidth
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

var options;

function show(d, merge = false) {
    console.log(d)
    node = d.nodes
    // var d = {nodes, links};
    console.log(d);
    options = option(cass, d);
    // options.series[0].fixed = false;
    app.setOption(options, merge);
    options.series[0].fixed = true;
    setTimeout(() => {
        app.setOption(options)
    }, 1000)
    window.onresize  = () => {
        app.setOption(options)
    }

}



