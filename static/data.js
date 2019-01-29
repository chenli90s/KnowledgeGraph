let nodes = []

let items = {};


let current = '';

let vue = null;

async function get_data(cas) {
    return new Promise(resolve => {
        axios.get('/relaction', {params: {cas}})
            .then(resp => {
                resolve(resp.data.data)
            })
    })
}

app.on('click', async function (params) {
    let cas = params.name
    console.log(params)
    console.log(!items[cas])

    if (!items[cas]) {
        data = await get_data(cas)
        items[cas] = data
    }

    document.getElementById('info').style.display = 'table'


    if(!vue){
        vue = initVue(items[cas].items)
    }

    current = cas

    show(loadingData(items[cas], cas, []))

});


app.on('dblclick', function (params) {
    // 控制台打印数据的名称
    console.log(params.name);
    let cas = params.name.split(':')
    if (!(cas.length > 1)) {
        // console.log('====')
        axios.get('/relaction', {params: {cas: params.name}})
            .then(resp => {
                let data = resp.data.data
                items[params.name] = data
                show(loadingData(data, params.name, keys))
            })
    }
});

app.on('mouseup', function (params) {
        console.log(params)
        let option = app.getOption();
        option.series[0].data[params.dataIndex].x = params.event.offsetX;
        option.series[0].data[params.dataIndex].y = params.event.offsetY;
        option.series[0].data[params.dataIndex].fixed = true;
        app.setOption(option);
    });


function search() {
    let cas = document.getElementById('cas')
    // keys.splice(0, keys.length)
    // nodes.splice(0, nodes.length)
    // links.splice(0, links.length)
    // app.showLoading();
    axios.get('/relaction', {params: {cas: cas.value}})
        .then(resp => {
            // app.hideLoading();
            let data = resp.data.data
            items[cas.value] = data
            // let d = loadingData(data, cas.value, [])
            // show(d, true)

            let d = chart.loadingData(data, cas.value)
            chart.show(d, true)
        })

}


const label = ['基本信息',
    '制备方法', '合成制备方法', '用途简介', '用途', '物化性质',
    '安全信息', '海关数据', '分子结构数据', '计算化学数据'];


function initVue(item) {
    let ks = []
    let vs = []
    // label.forEach((value, index) => {
    //     console.log(value)
    //     if(item[index].trim()){
    //         ks.push(value)
    //         vs.push(item[index])
    //     }
    // })

    console.log(ks)

    return new Vue({
        el: '#info',
        data: {
            keys: ks,
            vals: vs
        },
        methods: {
            handleClick(e, s) {
            },
            sync_btn() {
                console.log(items[current])
                let data = gen_synt(items[current], [])
                show(data, true)
            },
            ups_btn() {
                console.log(items[current])
                let data = gen_updowns(items[current], current, [], 'ups')
                show(data, true)
            },
            downs_btn() {
                console.log(items[current])
                let data = gen_updowns(items[current], current, [], 'downs')
                show(data, true)
            }
        }
    })
}




