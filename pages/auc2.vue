<template>
  <div class="container">
    <header class="py-3">
      <div
        class="d-flex flex-column flex-md-row align-items-center justify-content-between"
      >
        <h1 class="my-0 mr-md-auto">Auction House 2</h1>
      </div>
    </header>

    <div class="container mt-3">
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search items..."
          v-model="searchQuery"
        />
      </div>
      <div class="row">
        <div class="col-4" v-for="item in paginatedItems" :key="item.itemId">
          <div class="card mb-3">
            <img :src="item.itemPicture" class="card-img-top" alt="..." />
            <div class="card-body">
              <h5 class="card-title">{{ item.itemName }}</h5>
              <p class="card-text">Price: ${{ item.itemPrice }}</p>
              <button class="btn btn-primary mr-2" @click="showBidModal(item)">
                Bid
              </button>
              <button class="btn btn-success" @click="buyItem(item)">
                Buy
              </button>
            </div>
          </div>
        </div>
      </div>
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

    <b-modal id="bidModal" :title="selectedItem.itemName" v-model="modal">
      <div class="form-group">
        <label for="bidAmount">Bid Amount</label>
        <input
          type="number"
          class="form-control"
          id="bidAmount"
          v-model="bidAmount"
        />
      </div>
      <template v-slot:modal-footer="{ hide }">
        <button type="button" class="btn btn-secondary" @click="hide">
          Close
        </button>
        <button type="button" class="btn btn-primary" @click="placeBid">
          Place Bid
        </button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  async mounted() {
    const ip = await this.$axios.$get("/items");
    this.items = ip;
    if (this.$route.query.itemid) {
      this.items.forEach((item) => {
        if (item.itemId == this.$route.query.itemid) {
          this.selectedItem = item;
          this.modal = true;
          this.bidAmount = item.itemPrice;
        }
      });
    }
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
  computed: {
    filteredItems() {
      const searchQuery = this.searchQuery.toLowerCase();
      return this.items.filter((item) => {
        return item.itemName.toLowerCase().includes(searchQuery);
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
      currentPage: 1,
      itemsPerPage: 6,
      items: [
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
      selectedItem: { itemName: "" },
      bidAmount: 0,
      modal: false,
      searchQuery: "",
    };
  },
  methods: {
    showBidModal(item) {
      this.selectedItem = item;
      this.bidAmount = item.itemPrice;
      this.modal = true;
    },
    placeBid() {
      if (this.bidAmount <= this.selectedItem.itemPrice) {
        alert("Bid amount must be higher than current price");
      } else {
        this.selectedItem.itemPrice = this.bidAmount;
        this.modal = false;
      }
    },
    buyItem(item) {
      this.$bvModal
        .msgBoxConfirm(`Are you sure you want to buy ${item.itemName}?`, {
          title: "Buy Item",
          size: "sm",
          buttonSize: "sm",
          okVariant: "success",
          okTitle: "Yes",
          cancelTitle: "No",
          cancelVariant: "danger",
        })
        .then(async (value) => {
          if (value) {
            await this.$axios.$delete(`/item?itemId=${item.itemId}`);
            alert(`Congratulations! You bought ${item.itemName}`);
          }
        });
    },
  },
};
</script>
