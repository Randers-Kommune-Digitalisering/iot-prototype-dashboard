import { createApp } from 'vue';
import '@/assets/style.css';
import App from './App.vue';
import router from './router';
import { useSettings } from '@/settingsStore.js';
import plainTextDirective from './plainTextDirective.js';

(async () => {
	const { loadSettingsFromServer } = useSettings()
	// attempt to load remote settings; fall back to defaults on failure
	await loadSettingsFromServer()

	const app = createApp(App);
	app.use(router);

	// register global directive for plain-text contenteditable
	app.directive('plain-text', plainTextDirective);
	app.mount('#app');
})();
