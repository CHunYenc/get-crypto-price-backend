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
        { index: 3, href: '/login/', name: '登入' }
      ]
    };
  },
  created() {
    this.path_name = window.location.pathname;
    if (this.path_name === '/404') return;
    if (this.path_name === '/500') return;
    this.activeIndex = this.path_list.find((e) => e.href === this.path_name).index;
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
});

// alert("HELLO")
