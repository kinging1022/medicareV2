<template>
  <button :class="['btn', variant, customClass]">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    variant: {
      type: String,
      default: 'defaultValue', 
    },
    customClass: {
      type: String,
      default: '',
    },
  },
  methods: {
   
  }
};
</script>

<style scoped>
.btn {
  padding: 0.5rem 1rem; 
  cursor: pointer;
}
</style>

  