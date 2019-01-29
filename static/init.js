const app = echarts.init(document.getElementById('container'))
const cass = [{name: '350-03-8'}, {name: 'ups'}, {name: 'downs'}, {name: '合成路线'}];
const keys = [];
// const nodes = [];
// const links = [];
// const prefix = 'image://';

// var data = {'synts': [{'front': [{'cas': '55676-25-0', 'url': 'http://data.huaxuejia.cn/casimg/676/55676-25-0.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~98%'}, {'front': [{'cas': '52155-97-2', 'url': 'http://data.huaxuejia.cn/casimg/155/52155-97-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~95%'}, {'front': [{'cas': '32064-90-7', 'url': ''}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~92%'}, {'front': [{'cas': '4754-27-2', 'url': 'http://data.huaxuejia.cn/casimg/754/4754-27-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~92%'}, {'front': [{'cas': '6335-40-6', 'url': 'http://data.huaxuejia.cn/casimg/335/6335-40-6.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~90%'}, {'front': [{'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}, {'cas': '75-36-5', 'url': 'http://data.huaxuejia.cn/casimg/75/75-36-5.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~87%'}, {'front': [{'cas': '14188-94-4', 'url': 'http://data.huaxuejia.cn/casimg/188/14188-94-4.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~83%'}, {'front': [{'cas': '5973-84-2', 'url': 'http://data.huaxuejia.cn/casimg/973/5973-84-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~82%'}, {'front': [{'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}, {'cas': '111-34-2', 'url': 'http://data.huaxuejia.cn/casimg/111/111-34-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~82%'}, {'front': [{'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}, {'cas': '764-78-3', 'url': 'http://data.huaxuejia.cn/casimg/764/764-78-3.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~75%'}, {'front': [{'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}, {'cas': '109-92-2', 'url': 'http://data.huaxuejia.cn/casimg/109/109-92-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~70%'}, {'front': [{'cas': '2510-23-8', 'url': 'http://data.huaxuejia.cn/casimg/510/2510-23-8.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~69%'}, {'front': [{'cas': '626-60-8', 'url': 'http://data.huaxuejia.cn/casimg/626/626-60-8.png'}, {'cas': '111-34-2', 'url': 'http://data.huaxuejia.cn/casimg/111/111-34-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~66%'}, {'front': [{'cas': '106353-54-2', 'url': 'http://data.huaxuejia.cn/casimg/353/106353-54-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~57%'}, {'front': [{'cas': '106881-77-0', 'url': 'http://data.huaxuejia.cn/casimg/881/106881-77-0.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~51%'}, {'front': [{'cas': '614-18-6', 'url': 'http://data.huaxuejia.cn/casimg/614/614-18-6.png'}, {'cas': '141-78-6', 'url': 'http://data.huaxuejia.cn/casimg/141/141-78-6.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~48%'}, {'front': [{'cas': '536-78-7', 'url': 'http://data.huaxuejia.cn/casimg/536/536-78-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~28%'}, {'front': [{'cas': '30510-18-0', 'url': 'http://data.huaxuejia.cn/casimg/510/30510-18-0.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '152171-44-3', 'url': 'http://data.huaxuejia.cn/casimg/171/152171-44-3.png'}], 'pre': '~'}, {'front': [{'cas': '536-78-7', 'url': 'http://data.huaxuejia.cn/casimg/536/536-78-7.png'}, {'cas': '7664-93-9', 'url': 'http://data.huaxuejia.cn/casimg/664/7664-93-9.png'}, {'cas': '64-19-7', 'url': 'http://data.huaxuejia.cn/casimg/64/64-19-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '14188-94-4', 'url': 'http://data.huaxuejia.cn/casimg/188/14188-94-4.png'}, {'cas': '64-17-5', 'url': 'http://data.huaxuejia.cn/casimg/64/64-17-5.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '62-54-4', 'url': 'http://data.huaxuejia.cn/casimg/62/62-54-4.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '6965-62-4', 'url': 'http://data.huaxuejia.cn/casimg/965/6965-62-4.png'}, {'cas': '603-35-0', 'url': 'http://data.huaxuejia.cn/casimg/603/603-35-0.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '2065-66-9', 'url': ''}], 'pre': '~'}, {'front': [{'cas': '81977-63-1', 'url': 'http://data.huaxuejia.cn/casimg/977/81977-63-1.png'}, {'cas': '586-96-9', 'url': 'http://data.huaxuejia.cn/casimg/586/586-96-9.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '81977-60-8', 'url': 'http://data.huaxuejia.cn/casimg/977/81977-60-8.png'}], 'pre': '~'}, {'front': [{'cas': '875783-82-7', 'url': 'http://data.huaxuejia.cn/casimg/783/875783-82-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '65-85-0', 'url': 'http://data.huaxuejia.cn/casimg/65/65-85-0.png'}], 'pre': '~'}, {'front': [{'cas': '10472-95-4', 'url': 'http://data.huaxuejia.cn/casimg/472/10472-95-4.png'}, {'cas': '64-17-5', 'url': 'http://data.huaxuejia.cn/casimg/64/64-17-5.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '93-89-0', 'url': 'http://data.huaxuejia.cn/casimg/93/93-89-0.png'}], 'pre': '~'}, {'front': [{'cas': '93-60-7', 'url': 'http://data.huaxuejia.cn/casimg/93/93-60-7.png'}, {'cas': '64-19-7', 'url': 'http://data.huaxuejia.cn/casimg/64/64-19-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '536-78-7', 'url': 'http://data.huaxuejia.cn/casimg/536/536-78-7.png'}, {'cas': '64-19-7', 'url': 'http://data.huaxuejia.cn/casimg/64/64-19-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '108-24-7', 'url': 'http://data.huaxuejia.cn/casimg/108/108-24-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '676-58-4', 'url': 'http://data.huaxuejia.cn/casimg/676/676-58-4.png'}, {'cas': '95091-91-1', 'url': ''}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '123-91-1', 'url': 'http://data.huaxuejia.cn/casimg/123/123-91-1.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '78857-63-3', 'url': 'http://data.huaxuejia.cn/casimg/857/78857-63-3.png'}], 'pre': '~'}, {'front': [{'cas': '917-54-4', 'url': 'http://data.huaxuejia.cn/casimg/917/917-54-4.png'}, {'cas': '59-26-7', 'url': 'http://data.huaxuejia.cn/casimg/59/59-26-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '10400-19-8', 'url': 'http://data.huaxuejia.cn/casimg/400/10400-19-8.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '141-78-6', 'url': 'http://data.huaxuejia.cn/casimg/141/141-78-6.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '56129-55-6', 'url': 'http://data.huaxuejia.cn/casimg/129/56129-55-6.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '27854-93-9', 'url': 'http://data.huaxuejia.cn/casimg/854/27854-93-9.png'}], 'pre': '~'}, {'front': [{'cas': '56129-55-6', 'url': 'http://data.huaxuejia.cn/casimg/129/56129-55-6.png'}], 'back': [{'cas': '40154-75-4', 'url': 'http://data.huaxuejia.cn/casimg/154/40154-75-4.png'}, {'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '6283-81-4', 'url': 'http://data.huaxuejia.cn/casimg/283/6283-81-4.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '4754-27-2', 'url': 'http://data.huaxuejia.cn/casimg/754/4754-27-2.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}, {'cas': '5096-11-7', 'url': ''}], 'pre': '~'}, {'front': [{'cas': '100-54-9', 'url': 'http://data.huaxuejia.cn/casimg/100/100-54-9.png'}, {'cas': '917-64-6', 'url': 'http://data.huaxuejia.cn/casimg/917/917-64-6.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '760211-73-2', 'url': ''}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '64-19-7', 'url': 'http://data.huaxuejia.cn/casimg/64/64-19-7.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}, {'front': [{'cas': '477723-45-8', 'url': ''}], 'back': [{'cas': '350-03-8', 'url': 'http://data.huaxuejia.cn/casimg/350/350-03-8.png'}], 'pre': '~'}], 'updown': {'ups': [{'cas': '4754-27-2', 'url': 'http://data.huaxuejia.cn/casimg/754/4754-27-2.png'}, {'cas': '626-55-1', 'url': 'http://data.huaxuejia.cn/casimg/626/626-55-1.png'}, {'cas': '75-36-5', 'url': 'http://data.huaxuejia.cn/casimg/75/75-36-5.png'}, {'cas': '111-34-2', 'url': 'http://data.huaxuejia.cn/casimg/111/111-34-2.png'}, {'cas': '764-78-3', 'url': 'http://data.huaxuejia.cn/casimg/764/764-78-3.png'}], 'downs': [{'cas': '104501-58-8', 'url': 'http://data.huaxuejia.cn/casimg/501/104501-58-8.png'}, {'cas': '111781-56-7', 'url': 'http://data.huaxuejia.cn/casimg/781/111781-56-7.png'}, {'cas': '107445-24-9', 'url': 'http://data.huaxuejia.cn/casimg/445/107445-24-9.png'}, {'cas': '106881-77-0', 'url': 'http://data.huaxuejia.cn/casimg/881/106881-77-0.png'}, {'cas': '960622-18-8', 'url': ''}]}}

let data = []

function loadingData(data, cas, key) {
    // let keys = [];
    let nodes = [];
    let links = [];

    function genEleNode(v, cate) {
        if (key.indexOf(v.cas) < 0) {
            let symbol = v.url ? prefix + v.url : 'rect';
            nodes.push({name: v.cas, id: v.cas, symbol, category: cate, symbolSize: 50, label: {normal: {show: true}}})
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


function gen_synt(data, key) {

    let nodes = [];
    let links = [];

    function genEleNode(v, cate) {
        if (key.indexOf(v.cas) < 0) {
            let symbol = v.url ? prefix + v.url : 'rect';
            nodes.push({name: v.cas, id: v.cas, symbol, category: cate, symbolSize: 50, label: {normal: {show: true}}})
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

function gen_updowns(data, cas, key, updown) {
    let nodes = [];
    let links = [];
    function genEleNodes(v, cate) {
        if (key.indexOf(v.cas) < 0) {
            let symbol = v.url ? prefix + v.url : 'rect';
            nodes.push({name: v.cas, id: v.cas, symbol, category: cate, symbolSize: 50, label: {normal: {show: true}}})
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
