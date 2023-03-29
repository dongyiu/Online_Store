<template>
  <div class="input-group mb-3">
    <input type="text" class="form-control" placeholder="Search for products" v-model="searchTerm">
    <div class="input-group-append">
      <button class="btn btn-outline-secondary" type="button" @click="searchProducts">Search</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: ''
    }
  },
  methods: {
    searchProducts() {
      this.$emit('search', this.searchTerm);
    }
  }
}
</script>
