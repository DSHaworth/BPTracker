import EventBus from '@/eventBus'

export default new class {

/*
  snackbarService.showSuccess({
    text: "Record updated",
    timeout: 1000
  });     
*/

  showError(payload){

    let defaultParameters = {
      text: "Error",
      color: "red",
      show: true,
      timeout: 3000
    }

    EventBus.$emit('SNACKBAR', {
      ...defaultParameters,
      ...payload
    });         
  }

  showSuccess(payload){

    let defaultParameters = {
      text: "Success",
      color: "green",
      show: true,
      timeout: 3000
    }

    EventBus.$emit('SNACKBAR', {
      ...defaultParameters,
      ...payload
    });
  }

  showInfo(payload){

    let defaultParameters = {
      text: "Info",
      color: "blue",
      show: true,
      timeout: 3000
    }

    EventBus.$emit('SNACKBAR', {
      ...defaultParameters,
      ...payload
    });         
  }  
}