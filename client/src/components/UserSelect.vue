<template>
    <div class="initials">
        {{user.firstname[0]}}{{user.lastname[0]}}
    </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    user: {
        type: Object, 
        required: true
    }
  }
}
</script>

<style scoped lang="scss">
//https://codepen.io/AllThingsSmitty/pen/dWmmQp
$container_size: 5rem;
$font_size: 2.5rem;

.initials {
    background: #099bdd;
    color: white;
    opacity: 1; 
    display: inline-block; 
    //font-size: calc(var($container_size) / 2);
    font-size: $font-size;
    border-radius: 50%; 
    vertical-align: middle; 
    margin-right: 0.5em; 
    width: $container_size; 
    height: $container_size; 
    line-height: $container_size; 
    text-align: center; 
}
</style>