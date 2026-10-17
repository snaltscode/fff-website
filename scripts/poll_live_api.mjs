async function poll() {
  console.log('Polling https://founderforfounder.in/api ...');
  for (let i = 0; i < 20; i++) {
    try {
      const res = await fetch('https://founderforfounder.in/api');
      const ct = res.headers.get('content-type') || '';
      console.log(`[Attempt ${i + 1}] /api Status: ${res.status} Content-Type: ${ct}`);
      if (res.status === 200) {
        const json = await res.json();
        console.log('API Healthcheck Success:', json);

        // Also test /api/public/content
        const resContent = await fetch('https://founderforfounder.in/api/public/content');
        console.log(`/api/public/content Status: ${resContent.status}`);
        if (resContent.status === 200) {
          const contentJson = await resContent.json();
          console.log('/api/public/content Keys:', Object.keys(contentJson));
          return;
        }
      }
    } catch (e) {
      console.log(`[Attempt ${i + 1}] Error: ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 6000));
  }
}
poll();
