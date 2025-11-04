class LeoCore < Formula
  include Language::Python::Virtualenv

  desc "LEO Core — AI Visibility Scoring Engine (LangGraph + FastAPI + MCP)"
  homepage "https://github.com/Yesh48/LEOlabs"
  url "https://github.com/Yesh48/LEOlabs/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    bin.install "leo-core/cli.py" => "leo"
  end

  def caveats
    <<~EOS
      LEO Core installed successfully!
      To use semantic scoring, set your API key:
        export OPENAI_API_KEY=your_key_here
    EOS
  end

  test do
    system "#{bin}/leo", "--help"
  end
end
