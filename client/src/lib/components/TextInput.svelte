<script lang="ts">
  let {
    label = "",
    value = $bindable(),
    update = () => {},
    placeholder = "",
  } = $props<{
    label?: string;
    value?: string;
    update?: () => void;
    placeholder?: string;
  }>();

  let timeoutId: number | null = null;

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;

    // Debounce the update call
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = window.setTimeout(() => {
      update();
    }, 500); // Adjust debounce delay as needed (e.g., 500ms)
  }
</script>

<div class="mb-4">
  <label class="block text-gray-700 text-sm font-bold mb-2" for={label}>
    {label}
  </label>
  <input
    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
    id={label}
    type="text"
    bind:value
    oninput={handleInput}
    {placeholder}
  />
</div>
