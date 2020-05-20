import * as AuthSession from "expo-auth-session";
import * as React from "react";
import { Button, Image, Platform, StyleSheet, Text, View } from "react-native";

const FB_APP_ID = "672636582940821";
const DJANGO_PUBLIC_URL = 'https://example.com'
import * as WebBrowser from 'expo-web-browser';
import { WebView } from 'react-native-webview';


WebBrowser.maybeCompleteAuthSession();


// Endpoint
const discovery = {
  authorizationEndpoint: "https://www.facebook.com/v6.0/dialog/oauth",
  tokenEndpoint: "https://graph.facebook.com/v6.0/oauth/access_token",
};

const useProxy = Platform.select({ web: false, default: true });

export default function App() {
  const [user, setUser] = React.useState(null);

  const redirectUri = AuthSession.makeRedirectUri({
    useProxy,
    // For usage in bare and standalone
    // Use your FBID here. The path MUST be `authorize`.
    native: `fb${FB_APP_ID}://authorize`,
  });

  // Request
  const [request, response, promptAsync] = AuthSession.useAuthRequest(
    {
      clientId: FB_APP_ID,
      scopes: ["public_profile", "user_likes"],
      // For usage in managed apps using the proxy
      redirectUri,
      extraParams: {
        // Use `popup` on web for a better experience
        display: Platform.select({ web: "popup" }),
        // Optionally you can use this to rerequest declined permissions
        auth_type: "rerequest",
      },
      // NOTICE: This has been changed to Code
      // https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/#confirm
      responseType: AuthSession.ResponseType.Code,
    }, discovery);

  // You need to add this url to your authorized redirect urls on your Facebook app
  console.log({
    redirectUri,
    useProxy,
  });

  const _handlePressAsync = async () => {
    const result = await promptAsync({ useProxy });

    if (result.type !== "success") {
      alert("Uh oh, something went wrong");
      return;
    }
    console.log(result)
    // Start dj-rest-auth token exchange
    let accessToken = result.params.accessToken;
    let code = result.params.code;
    console.log('Access token:', accessToken);
    console.log('Code:', code);

    let tokenExchangeResponse = await fetch(
        DJANGO_PUBLIC_URL+'/dj-rest-auth/facebook/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code }),
        }
    );
    const res = await tokenExchangeResponse.json();
    console.log('Result is:', res);
    const {
        access_token,
        refresh_token,
        user: djangoUserInfo
    } = res;
    console.log(access_token)

    let user = await fetch(
        DJANGO_PUBLIC_URL+'/dj-rest-auth/user/',
        {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token,
            },
        },
    );
    let userJson = await user.json();
    console.log('REST auth call:', userJson);
    // End dj-rest-auth token exchange

    setUser(access_token);
  };

  let handleWebViewNavigationStateChange = newNavState => {
    console.log(newNavState)
  }

    const runFirst = `
      document.body.style.backgroundColor = 'red';
      setTimeout(function() { alert(access_token); }, 2000);
      window.access_token = "${user}";
      true; // note: this is required, or you'll sometimes get silent failures
    `;

  return (
    <View style={styles.container}>
      {user ? (
        <WebView
          source={{ uri: DJANGO_PUBLIC_URL + '/map'}}
          style={{ flex: 1 }}
          injectedJavaScript={runFirst}
          onNavigationStateChange={handleWebViewNavigationStateChange}
        />
      ) : (
        <Button
          disabled={!request}
          title="Open FB Auth"
          onPress={_handlePressAsync}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor:'blue',
    flex: 1,
    // Warning: Browser has zero width if this is uncommented
    // alignItems: "center",
    justifyContent: "center",
  },
  profile: {
    alignItems: "center",
  },
  name: {
    fontSize: 20,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: 50,
  },
});
