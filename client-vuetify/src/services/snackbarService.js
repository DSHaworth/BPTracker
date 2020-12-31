import EventBus from '@/eventBus'

export default new class {

    showError(payload){
        EventBus.$emit('SNACKBAR', {
            text: payload.text,
            color: "red",
            show: true,
            timeout: 3000
          });         
    }

    showSuccess(payload){
        EventBus.$emit('SNACKBAR', {
            text: payload.text,
            color: "green",
            show: true,
            timeout: 3000
          });         
    }
}