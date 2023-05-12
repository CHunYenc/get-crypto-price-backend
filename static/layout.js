var header = new Vue({
  el: '#header',
  delimiters: ['[[', ']]'],
  data() {
    return {
      activeIndex: '1',
      path_name: null,
      path_list: [
        { index: 1, href: '/', name: '首頁' },
        { index: 2, href: '/pricing/', name: '即時報價' },
        // { index: 3, href: '/login/', name: '登入', disabled: true },
      ]
    };
  },
  created() {
    this.path_name = window.location.pathname;
    if (this.path_name === '/404') return;
    if (this.path_name === '/500') return;
    this.activeIndex = this.path_list.find((e) => e.href === this.path_name).index;
  },
  mounted() {
    const alerts = document.getElementsByClassName('alert');
    const alerts_parent = alerts[0].parentElement;
    if (alerts.length === 0) return;
    setTimeout(() => {
      alerts_parent.style.display = 'none';
    }, 2000); // 延遲 2000 毫秒（2 秒）後執行
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
});

// alert("HELLO")
