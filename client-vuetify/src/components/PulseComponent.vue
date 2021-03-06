<template>
  <v-tabs background-color="deep-purple accent-4" dark style="padding: 20px">
    <v-tabs-slider color="yellow"></v-tabs-slider>

    <v-tab href="#table">
      <v-icon left> mdi-table </v-icon>
      Table
    </v-tab>
    <v-tab-item value="table">
      <v-sheet color="white" elevation="2" style="padding: 10px; margin: 10px">
        <v-toolbar flat>
          <v-toolbar-title
            >{{ currentUser.firstname }}
            {{ currentUser.lastname }}</v-toolbar-title
          >
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            elevation="2"
            fab
            small
            @click="onShowCreate()"
          >
            <v-icon dark> mdi-plus </v-icon>
          </v-btn>
        </v-toolbar>

        <v-data-table
          :headers="headers"
          :items="userPulseStats"
          :items-per-page="5"
          :custom-sort="customSort"
          class="elevation-1"
          :loading="loading"
          loading-text="Loading... Please wait"
        >
          <template v-slot:item.recordDateTime="{ item }">
            <span>{{ new Date(item.recordDateTime).toLocaleString() }}</span>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>
        </v-data-table>

        <pulse-add-edit-dialog
          :showDialog="showDialog"
          :formTitle="formTitle"
          :item="editedItem"
          v-on:close-create="onCloseCreate"
        />
        <delete-confirm
          :showDeleteDialog="showDeleteDialog"
          @cancel-delete="deleteClose"
          @confirm-delete="deleteConfirm"
        />
      </v-sheet>
    </v-tab-item>

    <v-tab href="#chart">
      <v-icon left> mdi-chart-box-outline </v-icon>
      Chart
    </v-tab>
    <v-tab-item value="chart">
      <PulseChart />
    </v-tab-item>
  </v-tabs>
</template>

<script>
import { mapState, mapGetters } from "vuex";

import PulseAddEditDialog from "@/components/PulseAddEditDialog.vue";
import PulseChart from "@/components/PulseChart.vue";
import DeleteConfirm from "@/components/DeleteConfirm.vue";

import snackbarService from "@/services/snackbarService";
import commonService from "@/services/commonService";
import EventBus from "@/eventBus";

export default {
  name: "PulseComponent",
  data() {
    return {
      showDialog: false,
      showDeleteDialog: false,
      loading: false,
      editedItem: {
        pulseId: 0,
        userId: 0,
        recordDate: "",
        recordTime: "",
        pulse: "",
        activity: "",
        notes: "",
      },
      defaultItem: {
        pulseId: 0,
        userId: 0,
        recordDate: "",
        recordTime: "",
        pulse: null,
        activity: "",
        notes: "",
      },
      headers: [
        {
          text: "Date",
          value: "recordDateTime",
          sortable: false,
          width: "12rem",
        },
        { text: "Pulse", value: "pulse", sortable: false, width: "4rem" },
        { text: "Activity", value: "activity", sortable: false, width: "9rem" },
        { text: "Notes", value: "notes", sortable: false },
        { text: "Actions", value: "actions", sortable: false, align: "end" },
      ],
    };
  },
  computed: {
    ...mapState({ currentUser: "user" }),
    ...mapGetters(["userPulseStats"]),
    formTitle() {
      return this.editedItem.pulseId === 0 ? "Add Item" : "Edit Item";
    }
  },
  methods: {
    // Table Actions
    onShowCreate: function () {
      this.editedItem = this.defaultItem;

      var d = new Date();
      this.defaultItem.recordTime = `${d.getHours()}:${(
        "0" + d.getMinutes()
      ).slice(-2)}`;
      this.defaultItem.recordDate = `${d.getFullYear()}-${
        d.getMonth() + 1
      }-${d.getDate()}`;
      this.editedItem.userId = this.currentUser.userId;

      this.showDialog = true;
    },
    editItem(item) {
      this.editedItem = Object.assign({}, item);

      var d = new Date(item.recordDateTime);
      this.editedItem.recordTime = `${d.getHours()}:${d.getMinutes()}`;
      this.editedItem.recordDate = `${d.getFullYear()}-${
        d.getMonth() + 1
      }-${d.getDate()}`;
      this.editedItem.userId = this.currentUser.userId;

      this.showDialog = true;
    },
    onCloseCreate: function () {
      this.showDialog = false;
    },
    getUserPulseStats: function () {
      this.loading = true;
      this.$store
        .dispatch("getPulseStat", this.currentUser.userId)
        .then(() => {})
        .catch((error) => {
          if (error.response.status === 401) {
            EventBus.$emit("REAUTHENTICATE", this.getUserPulseStats);
          } else {
            snackbarService.showError({
              text: error.response.data.detail,
            });
          }
        })
        .then(() => {
          this.loading = false;
        });
    },
    // DELETE START
    deleteItem(item) {
      this.editedItem = Object.assign({}, item);
      this.editedItem.userId = this.currentUser.userId;
      this.showDeleteDialog = true;
    },
    deleteClose() {
      this.showDeleteDialog = false;
    },
    deleteConfirm() {
      this.loading = true;
      this.$store
        .dispatch("deletePulseStat", this.editedItem)
        .then(() => {
          snackbarService.showSuccess({
            text: "Pulsee stat removed",
          });
        })
        .catch((err) => {
          snackbarService.showError({
            text: err.response.data.detail,
          });
        })
        .then(() => {
          this.loading = false;
          this.closeDelete();
        });
    },
    //https://codepen.io/mmia/pen/jOPyXad?editors=1010
    customSort: function (items, index, isDesc) {
      this.userPulseStats.sort((a, b) => {
        if (index[0] == "recordDateTime") {
          if (!isDesc[0]) {
            return new Date(b[index]) - new Date(a[index]);
          } else {
            return new Date(a[index]) - new Date(b[index]);
          }
        } else {
          if (typeof a[index] !== "undefined") {
            if (!isDesc[0]) {
              return a[index]
                .toLowerCase()
                .localeCompare(b[index].toLowerCase());
            } else {
              return b[index]
                .toLowerCase()
                .localeCompare(a[index].toLowerCase());
            }
          }
        }
      });
      return items;
    },
  },
  components: {
    PulseChart,
    DeleteConfirm,
    PulseAddEditDialog,
  },
  created() {
    this.getUserPulseStats();
  },
};
</script>

<style lang="scss" scoped>
</style>