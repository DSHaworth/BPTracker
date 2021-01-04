<template>
    <v-dialog v-model="showDeleteDialog" max-width="500px">
        <v-card>
        <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="deleteClose">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="deleteConfirm">OK</v-btn>
            <v-spacer></v-spacer>
        </v-card-actions>
        </v-card>
    </v-dialog>  
</template>

<script>
export default {
  name: 'showDeleteDialog',
  props: {
    showDeleteDialog: Boolean,    
  },
  methods: {
    deleteClose () {
        this.$emit('cancel-delete')
    },      
    deleteConfirm(){
        this.$emit('confirm-delete')
    }
  }
}
</script>

<style lang="scss" scoped>

</style>