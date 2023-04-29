<template>
  <div class="container">
    <b-navbar toggleable="lg" type="light" variant="light" class="mb-3">
      <b-navbar-brand href="#">Online Store</b-navbar-brand>
    </b-navbar>

    <div class="container mt-3">
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search items..."
          v-model="searchQuery"
        />
        <div class="input-group-append">
          <button
            class="btn btn-success"
            type="button"
            @click="newItemModal = !newItemModal"
          >
            New Item
          </button>
        </div>
      </div>
      <transition-group tag="div" name="slide" class="d-flex flex-wrap">
        <div
          class="col-12 col-sm-6 col-md-4 col-lg-3"
          v-for="item in paginatedItems"
          :key="item.itemId"
        >
          <div class="card mb-3 item-card" @dblclick="deleteItem(item)">
            <img
              :src="item.itemPicture"
              @error="setFallbackImage"
              class="card-img-top"
              alt="..."
            />
            <div class="card-body">
              <h5 class="card-title">{{ item.itemName }}</h5>
              <p class="card-text">{{ item.item_description }}</p>
              <p class="card-text">Price: ${{ item.itemPrice }}</p>
              <button class="btn btn-success" @click="buyNow(item)">Buy</button>
            </div>
          </div>
        </div>
      </transition-group>
      <div class="d-flex justify-content-center">
        <b-pagination
          v-model="currentPage"
          :total-rows="filteredItems.length"
          :per-page="itemsPerPage"
          align="center"
          size="md"
          class="my-3"
        ></b-pagination>
      </div>
    </div>

    <b-modal v-model="showBuyModal" title="Buy From the Following Option">
      <div class="md-4 justify-content-center">
        <div>
          Online Store<b-button
            @click="buyItem"
            class="m-2"
            variant="success"
            size="l"
            >Buy &rarr;</b-button
          >
        </div>
        <div>
          Auction Store 1<a :href="`/auc?itemid=${selectedItem.itemId}`"
            ><b-button class="m-2" variant="success" size="l"
              >Buy &rarr;</b-button
            ></a
          >
        </div>
        <div>
          Auction Store 2<a :href="`/auc2?itemid=${selectedItem.itemId}`"
            ><b-button class="m-2" variant="success" size="l"
              >Buy &rarr;</b-button
            ></a
          >
        </div>
      </div>
    </b-modal>

    <b-modal v-model="newItemModal" title="Add a new item" @ok="handleNewItem">
      <div class="md-4 justify-content-center">
        <b-form-input
          class="mt-2"
          v-model="newItem.name"
          placeholder="Enter item name"
        ></b-form-input>
        <b-form-input
          class="mt-2"
          v-model="newItem.price"
          type="number"
          placeholder="Enter item price"
        ></b-form-input>
        <b-form-input
          class="mt-2"
          v-model="newItem.link"
          placeholder="Enter item image link"
        ></b-form-input>
      </div>
    </b-modal>

    <b-modal
      v-model="authorisedModal"
      title="Enter the username and password to perform this action."
      @ok="handleAuthorised"
    >
      <div class="md-4 justify-content-center">
        <b-form-input
          type="text"
          class="mt-2"
          v-model="authorised.username"
          placeholder="Enter username"
        ></b-form-input>
        <b-form-input
          type="password"
          class="mt-2"
          v-model="authorised.password"
          placeholder="Enter password"
        ></b-form-input>
      </div>
    </b-modal>
  </div>
</template>

<style scoped>
.slide-enter-active {
  transition: all 0.5s ease;
}

.slide-leave-active {
  transition: all 0.5s ease;
}

.slide-enter,
.slide-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}
</style>

<script>
export default {
  computed: {
    filteredItems() {
      const searchQuery = this.searchQuery.toLowerCase();
      return this.items.filter((item) => {
        return item?.itemName.toString().toLowerCase().includes(searchQuery);
      });
    },
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  data() {
    return {
      deleteItemModal: false,
      newItemModal: false,
      authorisedModal: false,
      defaultImageUrl: "https://via.placeholder.com/350x150",
      authorised: {},
      newItem: {},
      currentPage: 1,
      itemsPerPage: 8,
      items: [] || [
        {
          itemId: 1,
          itemName: "Item 1",
          itemPrice: 100,
          itemPicture: "https://via.placeholder.com/350x150",
        },
        {
          itemId: 2,
          itemName: "Item 2",
          itemPrice: 200,
          itemPicture: "https://via.placeholder.com/350x150",
        },
        {
          itemId: 3,
          itemName: "Item 3",
          itemPrice: 300,
          itemPicture: "https://via.placeholder.com/350x150",
        },
        {
          itemId: 4,
          itemName: "Item 4",
          itemPrice: 400,
          itemPicture: "https://via.placeholder.com/350x150",
        },
        {
          itemId: 5,
          itemName: "Item 5",
          itemPrice: 500,
          itemPicture: "https://via.placeholder.com/350x150",
        },
        {
          itemId: 6,
          itemName: "Item 6",
          itemPrice: 600,
          itemPicture: "https://via.placeholder.com/350x150",
        },
      ],
      showBuyModal: false,
      searchQuery: "",
      selectedItem: {},
      authorized: false,
    };
  },
  async mounted() {
    const ip = await this.$axios.$get("/items");
    this.items = ip;

    const ws = new WebSocket("ws://localhost:8080");

    ws.addEventListener("open", () => {
      console.log("Connected to websocket");
    });

    ws.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      console.log(message);
      if (
        message.type == "ADD" &&
        this.items.find((i) => i.itemId == message.item.itemId) == undefined
      ) {
        this.items.push(message.item);
      } else if (message.type == "DELETE") {
        this.items = this.items.filter((i) => i.itemId != message.itemId);
      }
    });
  },
  methods: {
    buyNow(product) {
      this.showBuyModal = true;
      this.selectedItem = product;
    },
    setFallbackImage(event) {
      event.target.src = this.defaultImageUrl;
    },
    deleteItem(item) {
      this.$bvModal
        .msgBoxConfirm(
          `Are you sure you want to delete item : ${item.itemName}?`
        )
        .then((value) => {
          if (value) {
            this.authorizeUser().then(async (authorized) => {
              if (authorized) {
                await this.$axios.$delete(`/item?itemId=${item.itemId}`);
                this.items = this.items.filter((i) => i.itemId !== item.itemId);
                alert(`Item ${item.itemName} deleted successfully!`);
              }
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleNewItem() {
      if (this.newItem.price < 1 || this.newItem.price > 100000) {
        alert("Price must be between 1 and 100,000");
        return;
      }
      if (!this.newItem.name || !this.newItem.price || !this.newItem.link) {
        alert("Please fill all the fields");
        return;
      }
      this.authorizeUser().then(async (authorized) => {
        if (authorized) {
          await this.$axios.$post(
            `/item?itemName=${this.newItem.name}&itemPrice=${this.newItem.price}&itemPicture=${this.newItem.link}`
          );
          // this.items.push({
          //   itemId: this.items.length + 1,
          //   itemName: this.newItem.name,
          //   itemPrice: this.newItem.price,
          //   itemPicture: this.newItem.link,
          // });
          this.newItemModal = false;
        }
      });
    },
    handleAuthorised() {
      if (
        this.authorised.username === "admin" &&
        this.authorised.password === "admin"
      ) {
        this.authorisedModal = false;
        this.authorized = true;
      } else {
        alert("Incorrect username or password");
      }
    },
    async authorizeUser() {
      if (this.authorized) {
        return true;
      }
      this.authorisedModal = true;
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(this.authorized);
        }, 15000);
        this.$watch("authorized", (newValue, oldValue) => {
          if (newValue) {
            resolve(newValue);
          }
        });
      });
    },
    buyItem() {
      this.showBuyModal = false;
      this.$bvModal
        .msgBoxConfirm(
          `Are you sure you want to buy item : ${this.selectedItem.itemName}?`
        )
        .then(async (value) => {
          if (value) {
            await this.$axios.$delete(
              `/item?itemId=${this.selectedItem.itemId}`
            );
            alert("Item bought successfully");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
