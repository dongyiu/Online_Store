<template>
    <div class="row">
      <div class="col-md-4" v-for="(product, index) in products" :key="index">
        <div class="card mb-4">
          <img :src="product.image" class="card-img-top" alt="Product image">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">${{ product.price }}</p>
            <button class="btn btn-primary" @click="buyNow(product)">Buy Now</button>
          </div>
        </div>
      </div>

      <b-modal v-model="showBuyModal" title="Buy From the Following Option">
      <div class="md-4 justify-content-center">
        <div>Online Store<b-button class="m-2" variant="success" size="l">Buy &rarr;</b-button></div>
        <div>Auction Store 1<b-button class="m-2" variant="success" size="l">Buy &rarr;</b-button></div>
        <div>Auction Store 2<b-button class="m-2" variant="success" size="l">Buy &rarr;</b-button></div>
      </div>
    </b-modal>

    </div>
  </template>
  
  <script>
  import { BModal, BButton } from 'bootstrap-vue';
  
  export default {
    data() {
      return {
        products: [
          { name: 'Product 1', price: 10.00, image: 'https://via.placeholder.com/300x200', itemId: '123' },
          { name: 'Product 2', price: 20.00, image: 'https://via.placeholder.com/300x200', itemId: '456' },
          { name: 'Product 3', price: 30.00, image: 'https://via.placeholder.com/300x200', itemId: '789' },
          { name: 'Product 4', price: 40.00, image: 'https://via.placeholder.com/300x200', itemId: '012' },
          { name: 'Product 5', price: 50.00, image: 'https://via.placeholder.com/300x200', itemId: '345' },
          { name: 'Product 6', price: 60.00, image: 'https://via.placeholder.com/300x200', itemId: '678' },
        ],
        showBuyModal: false,
      }
    },
    components: {
      BModal,
      BButton
    },
    methods: {
      buyNow(product) {
        this.showBuyModal = true;
      },
    }
  }
  </script>
  