<script lang="ts">
  /**
   * TextInput Component Props Interface
   *
   * @interface Props
   * @property {string} label - Display label for the input field
   * @property {string} value - Current input value (bindable)
   * @property {() => void} update - Optional callback fired after debounced input changes
   * @property {string} placeholder - Placeholder text for empty input
   */
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

  /**
   * Handle input changes with debouncing to avoid excessive API calls
   *
   * @param event - Input event from the text field
   */
  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;

    // Clear existing timeout to reset the debounce timer
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    // Set new timeout to call update after 500ms of no input
    timeoutId = window.setTimeout(() => {
      update();
    }, 500);
  }
</script>

<!--
  TextInput Component
  
  A debounced text input component that prevents excessive API calls while
  providing immediate visual feedback. Ideal for configuration settings
  that need to be synced with a backend server.
  
  Features:
  - Bindable value for two-way data binding
  - Debounced updates (500ms delay) to reduce API calls
  - Styled with Tailwind CSS for consistency
  - Proper accessibility with label association
  - Placeholder text support
-->
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
