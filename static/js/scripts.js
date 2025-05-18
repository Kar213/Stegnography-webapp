FilePond.create(document.querySelector("#filePayload"), {
    storeAsFile: true,
    server: null
});

function switchMode(mode) {
  document.getElementById('mode').value = mode;

  const encryptMode = mode === 'encrypt';

  document.getElementById('payloadSection').classList.toggle('hidden', !encryptMode);
  document.getElementById('encryptionOptions').classList.toggle('hidden', !encryptMode);
  document.getElementById('keyInputSection').classList.toggle('hidden', encryptMode);

  console.log('Mode switched to:', mode);
  console.log('payloadSection hidden:', document.getElementById('payloadSection').classList.contains('hidden'));
  console.log('encryptionOptions hidden:', document.getElementById('encryptionOptions').classList.contains('hidden'));
  console.log('keyInputSection hidden:', document.getElementById('keyInputSection').classList.contains('hidden'));
}

// Your existing event listeners...

// Remove or comment out the page reload after submit to avoid resetting mode unexpectedly
// document.getElementById('mainForm').addEventListener('submit', function() {
//   setTimeout(() => {
//     window.location.reload();
//   }, 1000); // reload 1 second after submit to reset form and UI
// });
