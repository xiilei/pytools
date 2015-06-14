package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"runtime"
	"time"
)

var transport = &http.Transport{
	Proxy: http.ProxyFromEnvironment,
	ResponseHeaderTimeout: 30 * time.Second,
}

type Server struct{}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())

	err := http.ListenAndServe(":8080", NewServer())
	if err != nil {
		fmt.Println(err.Error())
	}
}

func NewServer() *Server {
	return &Server{}
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// fmt.Println(r.Header.Get("Cookie"))
	// fmt.Println(r.RemoteAddr)
	saveCookies(r)
	resp, err := transport.RoundTrip(r)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	defer resp.Body.Close()
	dsth := w.Header()
	for k, vs := range resp.Header {
		for _, v := range vs {
			dsth.Add(k, v)
		}
	}
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}

func saveCookies(r *http.Request) {
	partial := fmt.Sprintf("Client:%s,Url:%s\n========\n%s",
		r.RemoteAddr, r.URL, r.Header.Get("Cookie"))
	ioutil.WriteFile("./save-cookies", []byte(partial), os.ModeAppend)
}
