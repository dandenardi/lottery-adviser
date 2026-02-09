#!/usr/bin/env node
/**
 * Script to automatically update the mobile API URL with the current local IP
 * Run this whenever your IP changes: node scripts/update-ip.js
 * 
 * This script filters out virtual network adapters (WSL, Hyper-V, VirtualBox)
 * and prioritizes physical Wi-Fi/Ethernet connections.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function getLocalIP() {
  try {
    // Get all network adapters with their IPs using PowerShell
    const output = execSync(
      'powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like \'192.168.*\'} | Select-Object IPAddress, InterfaceAlias | ConvertTo-Json"',
      { encoding: 'utf-8' }
    ).trim();

    if (output) {
      const adapters = JSON.parse(output);
      const adapterList = Array.isArray(adapters) ? adapters : [adapters];

      // Filter out virtual adapters (WSL, Hyper-V, VirtualBox, VMware, etc.)
      const virtualKeywords = ['vEthernet', 'WSL', 'Hyper-V', 'VirtualBox', 'VMware', 'vboxnet', 'Virtual'];
      const physicalAdapters = adapterList.filter(adapter => {
        const alias = adapter.InterfaceAlias || '';
        return !virtualKeywords.some(keyword => alias.includes(keyword));
      });

      if (physicalAdapters.length > 0) {
        // Prioritize Wi-Fi, then Ethernet
        const wifiAdapter = physicalAdapters.find(a => (a.InterfaceAlias || '').includes('Wi-Fi'));
        const ethernetAdapter = physicalAdapters.find(a => (a.InterfaceAlias || '').includes('Ethernet'));

        const selectedAdapter = wifiAdapter || ethernetAdapter || physicalAdapters[0];
        console.log(`📡 Using adapter: ${selectedAdapter.InterfaceAlias}`);
        return selectedAdapter.IPAddress;
      }
    }

    // Fallback: parse ipconfig output manually
    console.log('⚠️  PowerShell method failed, trying ipconfig fallback...');
    const ipconfig = execSync('ipconfig', { encoding: 'utf-8' });
    const lines = ipconfig.split('\n');

    // Look for Wi-Fi or Ethernet adapter sections (excluding virtual ones)
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Skip virtual adapters
      if (line.includes('vEthernet') || line.includes('Hyper-V') ||
        line.includes('VirtualBox') || line.includes('VMware')) {
        continue;
      }

      // Look for Wi-Fi or Ethernet adapter sections
      if (line.includes('Wi-Fi') || (line.includes('Ethernet') && !line.includes('vEthernet'))) {
        // Find IPv4 address in next few lines
        for (let j = i; j < Math.min(i + 10, lines.length); j++) {
          const match = lines[j].match(/IPv4.*?: (192\.168\.\d+\.\d+)/);
          if (match) {
            console.log(`📡 Using adapter from ipconfig: ${line.trim()}`);
            return match[1];
          }
        }
      }
    }

    throw new Error('Could not find local IP address on physical network adapter');
  } catch (error) {
    console.error('❌ Error getting local IP:', error.message);
    console.error('\n💡 Please manually set EXPO_PUBLIC_API_BASE_URL_MOBILE in .env file');
    console.error('   Example: EXPO_PUBLIC_API_BASE_URL_MOBILE=http://192.168.0.109:5000');
    process.exit(1);
  }
}

function updateEnvFile(ip) {
  const envPath = path.join(__dirname, '..', '.env');

  if (!fs.existsSync(envPath)) {
    console.error('❌ .env file not found!');
    process.exit(1);
  }

  let envContent = fs.readFileSync(envPath, 'utf-8');

  // Update the mobile API URL
  const mobileUrlRegex = /EXPO_PUBLIC_API_BASE_URL_MOBILE=http:\/\/[\d.]+:5000/;
  const newMobileUrl = `EXPO_PUBLIC_API_BASE_URL_MOBILE=http://${ip}:5000`;

  if (mobileUrlRegex.test(envContent)) {
    envContent = envContent.replace(mobileUrlRegex, newMobileUrl);
  } else {
    // If not found, add it
    envContent += `\n${newMobileUrl}\n`;
  }

  fs.writeFileSync(envPath, envContent, 'utf-8');

  console.log('✅ Updated .env file');
  console.log(`📱 Mobile API URL: http://${ip}:5000`);
  console.log('\n⚠️  Please restart your Expo dev server (npm start) for changes to take effect');
}

// Main
const localIP = getLocalIP();
console.log(`🔍 Detected local IP: ${localIP}`);
updateEnvFile(localIP);
