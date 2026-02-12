import { createApp } from 'vue';
import '@/assets/style.css';
import App from './App.vue';
import router from './router';
import { useSettings } from '@/settingsStore.js';

(async () => {
	const { loadSettingsFromServer } = useSettings()
	// attempt to load remote settings; fall back to defaults on failure
	await loadSettingsFromServer()

	const app = createApp(App);
	app.use(router);
	app.mount('#app');
})();
